from rest_framework import serializers
from app2.models import Role

class PageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"