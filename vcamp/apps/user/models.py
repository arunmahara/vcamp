from django.db import models
from django.contrib.postgres.fields import ArrayField
from vcamp.shared.models.timestamp import BaseModel


class User(BaseModel):
    email = models.EmailField(unique=True, db_index=True)
    name = models.CharField(max_length=64, null=True, blank=True)
    dp = models.URLField(null=True, blank=True)
    preferences = ArrayField(base_field=models.CharField(max_length=128), null=True, blank=True)
    allergies = ArrayField(base_field=models.CharField(max_length=128), null=True, blank=True)
    dietary_restrictions = ArrayField(base_field=models.CharField(max_length=128), null=True, blank=True)
    week_meal_plan = models.JSONField(null=True, blank=True)
    shopping_list_for_week = models.JSONField(null=True, blank=True)

    def __str__(self):
        return "{}".format(self.email)


class FCMDevice(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='fcm_device')
    fcm_token = models.TextField(max_length=350)

    def __str__(self):
        return str(self.fcm_token)
    

class Recipe(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_recipe')
    name = models.CharField(max_length=128)
    nutrition = ArrayField(base_field=models.CharField(max_length=128))
    ingredients = ArrayField(base_field=models.CharField(max_length=128))
    measurements = models.JSONField()
    process = models.JSONField()
    image = models.ImageField(upload_to='recipe/', null=True, blank=True)

    def __str__(self):
        return str(self.name)