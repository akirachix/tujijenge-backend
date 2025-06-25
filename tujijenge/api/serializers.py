from rest_framework import serializers
from users.models import Mamamboga
from users.models import Stakeholder
from stock.models import Product, Stock
from communities.models import Community
from communities.models import CommunityMembers
from communities.models import TrainingSessions
from communities.models import TrainingRegistration


class MamambogaSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Mamamboga
        fields ="__all__"

class StakeholderSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Stakeholder
        fields ="__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields= "__all__"
 
class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model=Stock
        fields= "__all__"

class CommunitySerializer(serializers.ModelSerializer):
    class Meta: 
        model = Community
        fields ="__all__"

class CommunityMembersSerializer(serializers.ModelSerializer):
    class Meta: 
        model = CommunityMembers
        fields ="__all__"
        
class TrainingSessionsSerializer(serializers.ModelSerializer):
    class Meta: 
        model = TrainingSessions
        fields ="__all__"
        
class TrainingRegistrationSerializer(serializers.ModelSerializer):
    class Meta: 
        model = TrainingRegistration
        fields ="__all__"

