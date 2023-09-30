from rest_framework import serializers
from vcamp.apps.user.models import User, Recipe


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ["name", "email", "dp", "preferences", "allergies", "dietary_restrictions"]
        read_only_fields = ["email", "dp"]


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe 
        fields = ["id", "name", "ingredients", "measurements", "process", "image"]