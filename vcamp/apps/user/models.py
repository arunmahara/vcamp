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

    def __str__(self):
        return "{}".format(self.email)