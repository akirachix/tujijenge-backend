from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.models import Mamamboga, Stakeholder
from .serializers import MamambogaSerializer, StakeholderSerializer
from django.shortcuts import get_object_or_404

class UserPolymorphicCRUDView(APIView):
    def get(self, request, pk=None):
        user_type = request.query_params.get('user_type')
        if pk:
            if user_type == 'mamamboga':
                user = get_object_or_404(Mamamboga, pk=pk)
                data = MamambogaSerializer(user).data
                data['user_type'] = 'mamamboga'
            elif user_type == 'stakeholder':
                user = get_object_or_404(Stakeholder, pk=pk)
                data = StakeholderSerializer(user).data
                data['user_type'] = 'stakeholder'
            else:
                return Response({"error": "user_type query param required for detail view"}, status=400)
            return Response(data)
        mamambogas = Mamamboga.objects.all()
        stakeholders = Stakeholder.objects.all()
        mamamboga_data = MamambogaSerializer(mamambogas, many=True).data
        for item in mamamboga_data:
            item['user_type'] = 'mamamboga'
        stakeholder_data = StakeholderSerializer(stakeholders, many=True).data
        for item in stakeholder_data:
            item['user_type'] = 'stakeholder'
        return Response(mamamboga_data + stakeholder_data)

    def post(self, request):
        user_type = request.data.get('user_type')
        if user_type == 'mamamboga':
            serializer = MamambogaSerializer(data=request.data)
        elif user_type == 'stakeholder':
            serializer = StakeholderSerializer(data=request.data)
        else:
            return Response({"error": "user_type must be either 'mamamboga' or 'stakeholder'."}, status=400)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=400)

    def put(self, request, pk=None):
        user_type = request.data.get('user_type')
        if not pk:
            return Response({"error": "pk required"}, status=400)
        if user_type == 'mamamboga':
            instance = get_object_or_404(Mamamboga, pk=pk)
            serializer = MamambogaSerializer(instance, data=request.data, partial=False)
        elif user_type == 'stakeholder':
            instance = get_object_or_404(Stakeholder, pk=pk)
            serializer = StakeholderSerializer(instance, data=request.data, partial=False)
        else:
            return Response({"error": "user_type must be either 'mamamboga' or 'stakeholder'."}, status=400)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def patch(self, request, pk=None):
        user_type = request.data.get('user_type')
        if not pk:
            return Response({"error": "pk required"}, status=400)
        if user_type == 'mamamboga':
            instance = get_object_or_404(Mamamboga, pk=pk)
            serializer = MamambogaSerializer(instance, data=request.data, partial=True)
        elif user_type == 'stakeholder':
            instance = get_object_or_404(Stakeholder, pk=pk)
            serializer = StakeholderSerializer(instance, data=request.data, partial=True)
        else:
            return Response({"error": "user_type must be either 'mamamboga' or 'stakeholder'."}, status=400)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk=None):
        user_type = request.data.get('user_type') or request.query_params.get('user_type')
        if not pk:
            return Response({"error": "pk required"}, status=400)
        if user_type == 'mamamboga':
            instance = get_object_or_404(Mamamboga, pk=pk)
        elif user_type == 'stakeholder':
            instance = get_object_or_404(Stakeholder, pk=pk)
        else:
            return Response({"error": "user_type must be either 'mamamboga' or 'stakeholder'."}, status=400)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)