from django.shortcuts import render
from rest_framework import viewsets, status 
from .serializers import MamambogaSerializer, StakeholderSerializer,CommunitySerializer, CommunityMembersSerializer, TrainingSessionsSerializer, TrainingRegistrationSerializer,OrderSerializer,ProductSerializer, StockSerializer
from communities.models import Community, CommunityMembers, TrainingSessions, TrainingRegistration
from orders.models import Order
from stock.models import Product, Stock
from rest_framework.response import Response
from django.db import IntegrityError
from users.models import Mamamboga, Stakeholder
from rest_framework.views import APIView
from .daraja import DarajaAPI
from .serializers import STKPushSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import logging
import requests
from django.shortcuts import get_object_or_404

from rest_framework.decorators import action


def haversine(lat1, lon1, lat2, lon2):
    R = 6371000
    leng = math.radians(lat1)
    leng2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2) ** 2 + \
        math.cos(leng) * math.cos(leng2) * math.sin(delta_lambda / 2) ** 2

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    meters = R * c
    return meters
    


USER_TYPES = {
    'mamamboga': (Mamamboga, MamambogaSerializer),
    'stakeholder': (Stakeholder, StakeholderSerializer),
}
geolocator = Nominatim(user_agent="tujijenge_backend")
logger = logging.getLogger(__name__)


class UnifiedUserViewSet(viewsets.ViewSet):
    def get_model_and_serializer(self, user_type):
        if user_type not in USER_TYPES:
            raise ValueError("Invalid user_type")
        return USER_TYPES[user_type]

    def list(self, request):
        user_type = request.query_params.get('user_type')
        if user_type and user_type in USER_TYPES:
            Model, Serializer = self.get_model_and_serializer(user_type)
            queryset = Model.objects.all()
            serializer = Serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            mamambogas = MamambogaSerializer(Mamamboga.objects.all(), many=True).data
            stakeholders = StakeholderSerializer(Stakeholder.objects.all(), many=True).data
            return Response(mamambogas + stakeholders)

    def retrieve(self, request, pk=None):
        user_type = request.query_params.get('user_type')
        if not user_type:
            try:
                instance = Mamamboga.objects.get(pk=pk)
                serializer = MamambogaSerializer(instance)
                return Response(serializer.data)
            except Mamamboga.DoesNotExist:
                try:
                    instance = Stakeholder.objects.get(pk=pk)
                    serializer = StakeholderSerializer(instance)
                    return Response(serializer.data)
                except Stakeholder.DoesNotExist:
                    return Response({'error': 'Not found'}, status=404)
        else:
            try:
                Model, Serializer = self.get_model_and_serializer(user_type)
                instance = Model.objects.get(pk=pk)
                serializer = Serializer(instance)
                return Response(serializer.data)
            except Exception:
                return Response({'error': 'Not found'}, status=404)

    def create(self, request):
        user_type = request.data.get('user_type')
        if not user_type:
            return Response({'error': 'user_type is required'}, status=400)
        try:
            Model, Serializer = self.get_model_and_serializer(user_type)
        except ValueError:
            return Response({'error': 'Invalid user_type'}, status=400)
        serializer = Serializer(data=request.data)
        if serializer.is_valid():
            try:
                instance = serializer.save()
                return Response(Serializer(instance).data, status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                return Response({'error': str(e)}, status=400)
        return Response(serializer.errors, status=400)

    def update(self, request, pk=None):
        user_type = request.data.get('user_type')
        if not user_type:
            return Response({'error': 'user_type is required'}, status=400)
        try:
            Model, Serializer = self.get_model_and_serializer(user_type)
            instance = Model.objects.get(pk=pk)
        except (ValueError, Model.DoesNotExist):
            return Response({'error': 'Not found'}, status=404)
        serializer = Serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                instance = serializer.save()
                return Response(Serializer(instance).data)
            except IntegrityError as e:
                return Response({'error': str(e)}, status=400)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        user_type = request.query_params.get('user_type')
        if not user_type:
            try:
                instance = Mamamboga.objects.get(pk=pk)
                instance.delete()
                return Response({'status': 'deleted'}, status=204)
            except Mamamboga.DoesNotExist:
                try:
                    instance = Stakeholder.objects.get(pk=pk)
                    instance.delete()
                    return Response({'status': 'deleted'}, status=204)
                except Stakeholder.DoesNotExist:
                    return Response({'error': 'Not found'}, status=404)
        else:
            try:
                Model, _ = self.get_model_and_serializer(user_type)
                instance = Model.objects.get(pk=pk)
                instance.delete()
                return Response({'status': 'deleted'}, status=204)
            except Exception:
                return Response({'error': 'Not found'}, status=404)

    @action(detail=False, methods=['post'], url_path='update-location')
    def update_location(self, request):
        user_id = request.data.get('id')
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')

        if not (user_id and latitude and longitude):
            return Response({'error': 'id, latitude and longitude required'}, status=status.HTTP_400_BAD_REQUEST)
        
        mamamboga = get_object_or_404(Mamamboga, id=user_id)
        mamamboga.latitude = float(latitude)
        mamamboga.longitude = float(longitude)
        geolocator = Nominatim(user_agent="tujijenge")
        try:
            location = geolocator.reverse((latitude, longitude), language="en")
            mamamboga.address = location.address if location and location.address else ''
        except Exception as e:
            mamamboga.address = ''
        
        mamamboga.save()
        return Response({'status': 'success', 'address': mamamboga.address}, status=status.HTTP_200_OK)        

    @action(detail=False, methods=['get'], url_path='communities-nearby')
    def communities_nearby(self, request):

        latitude = request.query_params.get('latitude')
        longitude = request.query_params.get('longitude')
        if not latitude or not longitude:
            return Response({'error': 'latitude and longitude are required'}, status=400)
        latitude = float(latitude)
        longitude = float(longitude)
        radius = 1000
        nearby = []
        for community in Community.objects.exclude(latitude__isnull=True, longitude__isnull=True):
            if community.latitude is not None and community.longitude is not None:
                distance = haversine(latitude, longitude, community.latitude, community.longitude)
                if distance <= radius:
                    nearby.append(CommunitySerializer(community).data)
        
        return Response(nearby)   




class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class CommunityViewSet(viewsets.ModelViewSet):
    queryset = Community.objects.all()
    serializer_class=CommunitySerializer
    
class CommunityMembersViewSet(viewsets.ModelViewSet):
    queryset = CommunityMembers.objects.all()
    serializer_class=CommunityMembersSerializer
    
class TrainingSessionsViewSet(viewsets.ModelViewSet):
    queryset = TrainingSessions.objects.all()
    serializer_class=TrainingSessionsSerializer
    
class TrainingRegistrationViewSet(viewsets.ModelViewSet):
    queryset = TrainingRegistration.objects.all()
    serializer_class=TrainingRegistrationSerializer
    

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
   

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
 

class STKPushView(APIView):
   def post(self, request):
       serializer = STKPushSerializer(data=request.data)
       if serializer.is_valid():
           data = serializer.validated_data
           daraja = DarajaAPI()
           response = daraja.stk_push(
               phone_number=data['phone_number'],
               amount=data['amount'],
               cart_item=data['cart_item'],
               account_reference=data['account_reference'],
               transaction_desc=data['transaction_desc']
           )
           return Response(response)
       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
def daraja_callback(request):
   print("Daraja Callback Data:", request.data)
   return Response({"ResultCode": 0, "ResultDesc": "Accepted"})