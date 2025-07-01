from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db import IntegrityError
from users.models import Mamamboga, Stakeholder
from .serializers import UnifiedUserSerializer

class UnifiedUserViewSet(viewsets.ViewSet):
    def get_object(self, user_type, pk):
        if user_type == 'mamamboga':
            return Mamamboga.objects.get(pk=pk)
        elif user_type == 'stakeholder':
            return Stakeholder.objects.get(pk=pk)
        else:
            raise ValueError("Unknown user_type")

    def list(self, request):
        user_type = request.query_params.get('user_type')
        if user_type == 'mamamboga':
            queryset = Mamamboga.objects.all()
        elif user_type == 'stakeholder':
            queryset = Stakeholder.objects.all()
        else:
            queryset = list(Mamamboga.objects.all()) + list(Stakeholder.objects.all())
        serializer = UnifiedUserSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        user_type = request.query_params.get('user_type')
        if not user_type:
            # Try to find in both
            try:
                instance = Mamamboga.objects.get(pk=pk)
            except Mamamboga.DoesNotExist:
                try:
                    instance = Stakeholder.objects.get(pk=pk)
                except Stakeholder.DoesNotExist:
                    return Response({'error': 'Not found'}, status=404)
        else:
            try:
                instance = self.get_object(user_type, pk)
            except Exception:
                return Response({'error': 'Not found'}, status=404)
        serializer = UnifiedUserSerializer(instance)
        return Response(serializer.data)

    def create(self, request):
        serializer = UnifiedUserSerializer(data=request.data)
        if serializer.is_valid():
            try:
                instance = serializer.save()
                serializer = UnifiedUserSerializer(instance)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                if "users_mamamboga.phone_number" in str(e):
                    return Response(
                        {"error": "Mamamboga with this phone number already exists."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                elif "users_stakeholder.phone_number" in str(e):
                    return Response(
                        {"error": "Stakeholder with this phone number already exists."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                elif "users_stakeholder.stakeholder_email" in str(e):
                    return Response(
                        {"error": "Stakeholder with this email already exists."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                return Response({"error": "Integrity error: " + str(e)}, status=400)
        return Response(serializer.errors, status=400)

    def update(self, request, pk=None):
        user_type = request.data.get('user_type')
        if not user_type:
            return Response({'error': 'user_type is required'}, status=400)
        try:
            instance = self.get_object(user_type, pk)
        except Exception:
            return Response({'error': 'Not found'}, status=404)
        serializer = UnifiedUserSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                instance = serializer.save()
                serializer = UnifiedUserSerializer(instance)
                return Response(serializer.data)
            except IntegrityError as e:
                return Response({"error": str(e)}, status=400)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        user_type = request.query_params.get('user_type')
        if not user_type:
            # Try both
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
                instance = self.get_object(user_type, pk)
                instance.delete()
                return Response({'status': 'deleted'}, status=204)
            except Exception:
                return Response({'error': 'Not found'}, status=404)