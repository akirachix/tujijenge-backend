from rest_framework import serializers
from users.models import Mamamboga
from users.models import Stakeholder

class MamambogaSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Mamamboga
        fields ="__all__"

class StakeholderSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Stakeholder
        fields ="__all__"