from rest_framework import serializers
from users.models import Mamamboga
from users.models import Stakeholder
from stock.models import Product, Stock


from payments.models import Order
from payments.models import Payment

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

<<<<<<< HEAD
=======
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields ="__all__"

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields ="__all__"

>>>>>>> 6213310ee00e80de1073f26d53c881cdd707763b

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

