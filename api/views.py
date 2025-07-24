from django.shortcuts import render
from rest_framework import viewsets, status 
from .serializers import MamambogaSerializer, StakeholderSerializer,CommunitySerializer, CommunityMembersSerializer, TrainingSessionsSerializer, TrainingRegistrationSerializer,OrderSerializer,ProductSerializer, StockSerializer, CartItemSerializer, CartSerializer
from communities.models import Community, CommunityMembers, TrainingSessions, TrainingRegistration
from orders.models import Order
from cart.models import Cart, CartItem
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
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
import math

from rest_framework.decorators import action, api_view


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


from users.models import Mamamboga, Stakeholder
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from users.permissions import IsMamamboga, IsStakeholder, StakeholderRolePermission

class UnifiedUserViewSet(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated] 
    def get_permissions(self):
        if self.action in ['create', 'login', 'register']:
            return [AllowAny()]
        
        elif self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return super().get_permissions()


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
        if user_type == 'mamamboga':
            first_name = request.data.get('first_name')
            last_name = request.data.get('last_name')
            phone_number = request.data.get('phone_number')
            pin = request.data.get('pin')

            if not all([first_name, last_name, phone_number, pin]):
                return Response({'error': 'All mamamboga fields required'}, status = 400)
            if User.objects.filter(username = phone_number).exists():
                return Response({'error': 'Phone number already registered'}, status=400)
            user = User.objects.create_user(
                username = phone_number,
                password = pin,
                first_name = first_name,
                last_name = last_name
            )
            Mamamboga.objects.create(
                user = user,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
            )
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=201)

        elif user_type == 'stakeholder':
            first_name = request.data.get('first_name')
            last_name = request.data.get('last_name')
            stakeholder_email = request.data.get('stakeholder_email')
            password = request.data.get('password_hash')  
            role = request.data.get('role')
            if not all([first_name, last_name, stakeholder_email, password, role]):
                return Response({'error': 'All stakeholder fields required'}, status=400)
            if User.objects.filter(username=stakeholder_email).exists():
                return Response({'error': 'Stakeholder email already registered'}, status=400)

            user = User.objects.create_user(
                username=stakeholder_email,
                email=stakeholder_email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            Stakeholder.objects.create(
                user=user,
                first_name=first_name,
                last_name=last_name,
                stakeholder_email=stakeholder_email,
                role=role,
            )
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user': user}, status=201)
        else:
            return Response({'error': 'Invalid user_type'}, status=400)

            



    @action(detail=False, methods=['post'], url_path='register', permission_classes=[AllowAny])
    def register(self, request):
        return self.create(request)

    def update(self, request, pk=None):
        user_type = request.data.get('user_type')
        if not user_type:
            return Response({'error': 'user_type is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            Model, Serializer = self.get_model_and_serializer(user_type)
        except Exception:
            return Response({'error': 'Invalid user_type'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            instance = Model.objects.get(pk=pk)
        except Model.DoesNotExist:
            return Response({'error': f'{user_type} with id {pk} not found'}, status=status.HTTP_404_NOT_FOUND)
        user = request.user
        if user_type == 'mamamboga' and hasattr(user, 'mamamboga'):
            if user.mamamboga.pk != instance.pk:
                return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        elif user_type == 'stakeholder' and hasattr(user, 'stakeholder'):
            if user.stakeholder.pk != instance.pk:
                return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        serializer = Serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data)
            except IntegrityError as e:
                return Response({'error': str(e)}, status=400)
        return Response(serializer.errors, status=400)


    
    @action(detail=False, methods=['post'], url_path='login', permission_classes=[AllowAny])
    def login(self, request):
        user_type = request.data.get('user_type')
        if user_type == 'mamamboga':
            phone_number = request.data.get('phone_number')
            pin = request.data.get('pin')
            if not (phone_number and pin):
                return Response({'error': 'phone_number and pin are required'}, status=400)

            user = authenticate(username=phone_number, password=pin)
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': token.key})
            else:
                return Response({'error': 'Invalid phone number or pin'}, status=401)

        elif user_type == 'stakeholder':
            stakeholder_email = request.data.get('stakeholder_email')
            password = request.data.get('password_hash')
            if not (stakeholder_email and password):
                return Response({'error': 'stakeholder_email and password are required'}, status=400)

            user = authenticate(username=stakeholder_email, password=password)
            
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                try:
                    stakeholder = Stakeholder.objects.get(user=user)
                    role = stakeholder.role
                except Stakeholder.DoesNotExist:
                    role = None
                return Response({'token': token.key, 'role': role, 'user': stakeholder_data})
            else:
                return Response({'error': 'Invalid email or password'}, status=401)

        else:
            return Response({'error': 'Invalid user_type'}, status=400)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
            return Response({"success": "Logged out successfully"}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"error": "Token not found"}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        user_type = request.query_params.get('user_type') or request.data.get('user_type')
        user = request.user

        if not user_type:
            return Response({'error': 'user_type is required'}, status=400)
        try:
            Model, _ = self.get_model_and_serializer(user_type)
            instance = Model.objects.get(pk=pk)
        except Exception:
            return Response({'error': 'Not found'}, status=404)

        if user_type == 'mamamboga' and hasattr(user, 'mamamboga'):
            if user.mamamboga.pk != instance.pk:
                return Response({'error': 'Permission denied'}, status=403)
        elif user_type == 'stakeholder' and hasattr(user, 'stakeholder'):
            if user.stakeholder.pk != instance.pk:
                return Response({'error': 'Permission denied'}, status=403)
        else:
            return Response({'error': 'Permission denied'}, status=403)

        instance.delete()
        return Response({'status': 'deleted'}, status=204)


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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsMamamboga()]
        elif self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return super().get_permissions()



    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'mamamboga'):
            return Order.objects.filter(mamamboga=user.mamamboga)
        stakeholder = getattr(user, 'stakeholder', None)
        if stakeholder and stakeholder.role == 'Supplier':
            return Order.objects.all()
        return Order.objects.none()


class CommunityViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Community.objects.all()
    serializer_class=CommunitySerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(), IsMamamboga()]
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return super().get_permissions()
 
class CommunityMembersViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = CommunityMembers.objects.all()
    serializer_class = CommunityMembersSerializer

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            return [IsAuthenticated(), IsMamamboga()]
        elif self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return super().get_permissions()

 
class TrainingSessionsViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = TrainingSessions.objects.all()
    serializer_class=TrainingSessionsSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), StakeholderRolePermission('Trainer')]
        elif self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return super().get_permissions()
  

class TrainingRegistrationViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = TrainingRegistration.objects.all()
    serializer_class = TrainingRegistrationSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(), IsMamamboga()]
        elif self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return super().get_permissions()


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), StakeholderRolePermission('Supplier')]
        elif self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return super().get_permissions()


  

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsMamamboga]

    def get_permissions(self):
        return [IsAuthenticated(), IsMamamboga()]
 

class STKPushView(APIView):
    permission_classes = [AllowAny]
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


  
class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsMamamboga]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsMamamboga()]
        elif self.action in ['list', 'retrieve']:
            return [IsAuthenticated(), IsMamamboga()]  
        return super().get_permissions()

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'mamamboga'):
            return Cart.objects.filter(mamamboga=user.mamamboga)
        return Cart.objects.none()




class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsMamamboga]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'mamamboga'):
            return CartItem.objects.filter(cart__mamamboga=user.mamamboga)
        return CartItem.objects.none()

    def perform_create(self, serializer):
        mamamboga = self.request.user.mamamboga
        cart = Cart.objects.filter(mamamboga=mamamboga).first()
        if not cart:
            cart = Cart.objects.create(mamamboga=mamamboga)

        product = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']
        cart_item = CartItem.objects.filter(cart=cart, product=product).first()
        if cart_item:
            cart_item.quantity += quantity
            cart_item.save()
            serializer.instance = cart_item  
        else:
            serializer.save(cart=cart)
   
    def perform_update(self, serializer):
        if serializer.instance.cart.mamamboga != self.request.user.mamamboga:
            raise PermissionDenied("You do not own this cart item.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.cart.mamamboga != self.request.user.mamamboga:
            raise PermissionDenied("You do not own this cart item.")
        instance.delete()
