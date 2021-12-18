from django.db.models import fields
from rest_framework.serializers import ModelSerializer
from base.models import Room


class room(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
