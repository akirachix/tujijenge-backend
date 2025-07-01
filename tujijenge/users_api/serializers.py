from rest_framework import serializers
from users.models import Mamamboga, Stakeholder

class UnifiedUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user_type = serializers.CharField(write_only=True)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    phone_number = serializers.CharField(max_length=20, required=False, allow_blank=True)
    pin = serializers.CharField(max_length=4, required=False, allow_blank=True)
    latitude = serializers.FloatField(required=False, allow_null=True)
    longitude = serializers.FloatField(required=False, allow_null=True)
    is_active = serializers.BooleanField(required=False)
    deactivation_date = serializers.DateTimeField(required=False, allow_null=True)
    certified_status = serializers.CharField(max_length=15, required=False, allow_blank=True)
    stakeholder_email = serializers.EmailField(max_length=255, required=False, allow_blank=True)
    password_hash = serializers.CharField(max_length=255, required=False, allow_blank=True)
    created_at = serializers.DateTimeField(read_only=True, required=False)
    updated_at = serializers.DateTimeField(read_only=True, required=False)
    user_type_output = serializers.SerializerMethodField('get_user_type', read_only=True)

    def get_user_type(self, obj):
        if isinstance(obj, Mamamboga):
            return "mamamboga"
        elif isinstance(obj, Stakeholder):
            return "stakeholder"
        return None

    def to_representation(self, instance):
        user = super().to_representation(instance)
        user['user_type'] = user.pop('user_type_output')
        return user

    def validate(self, data):
        user_type = data.get('user_type')
        if user_type == 'mamamboga':
            if not data.get('phone_number'):
                raise serializers.ValidationError({"phone_number": "This field is required for mamamboga."})
            if not data.get('pin'):
                raise serializers.ValidationError({"pin": "This field is required for mamamboga."})
        elif user_type == 'stakeholder':
            if not data.get('stakeholder_email'):
                raise serializers.ValidationError({"stakeholder_email": "This field is required for stakeholder."})
            if not data.get('password_hash'):
                raise serializers.ValidationError({"password_hash": "This field is required for stakeholder."})
        else:
            raise serializers.ValidationError({"user_type": "user_type must be 'mamamboga' or 'stakeholder'."})
        return data

    def create(self, validated_data):
        user_type = validated_data.pop('user_type')
        if user_type == 'mamamboga':
            return Mamamboga.objects.create(**validated_data)
        elif user_type == 'stakeholder':
            return Stakeholder.objects.create(**validated_data)
        else:
            raise serializers.ValidationError("Invalid user_type")

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if hasattr(instance, attr):
                setattr(instance, attr, value)
        instance.save()
        return instance