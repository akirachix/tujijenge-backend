from rest_framework import serializers # type: ignore
from communities.models import Community, CommunityMembers, TrainingSessions, TrainingRegistration

class CommunitySerializer(serializers.ModelSerializer):
    class Meta: 
        model = Community
        fields = "__all__"

class CommunityMembersSerializer(serializers.ModelSerializer):
    class Meta: 
        model = CommunityMembers
        fields = "__all__"
        
class TrainingSessionsSerializer(serializers.ModelSerializer):
    class Meta: 
        model = TrainingSessions
        fields = "__all__"
        
class TrainingRegistrationSerializer(serializers.ModelSerializer):
    class Meta: 
        model = TrainingRegistration
        fields = "__all__"