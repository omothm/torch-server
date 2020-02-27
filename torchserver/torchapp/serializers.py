from rest_framework import serializers
from torchapp.models import Banknote

class BanknoteSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    image_base64 = serializers.CharField()

    def create(self, validated_data):
        return Banknote.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.image_base64 = validated_data.get('image_base64', instance.image_base64)
        instance.save()
        return instance
