from rest_framework import serializers
from vcamp.apps.user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ["name", "email", "dp", "preferences", "allergies", "dietary_restrictions"]
        read_only_fields = ["email", "dp"]
