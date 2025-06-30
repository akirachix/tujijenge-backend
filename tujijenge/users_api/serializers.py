from rest_framework import serializers
from users.models import Mamamboga, Stakeholder

class MamambogaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mamamboga
        fields = '__all__'

class StakeholderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stakeholder
        fields = '__all__'

class PolymorphicUserSerializer(serializers.Serializer):
    user_type = serializers.ChoiceField(choices=[('mamamboga', 'Mamamboga'), ('stakeholder', 'Stakeholder')])
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        data = self.initial_data if hasattr(self, 'initial_data') else {}
        user_type = data.get('user_type')
        if user_type == 'mamamboga':
            for field in MamambogaSerializer().fields:
                if field != 'id': 
                    self.fields[field] = MamambogaSerializer().fields[field]
        elif user_type == 'stakeholder':
            for field in StakeholderSerializer().fields:
                if field != 'id':
                    self.fields[field] = StakeholderSerializer().fields[field]