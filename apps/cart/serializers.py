from rest_framework import serializers


class ItemSerializer(serializers.Serializer):
    """
    Serializer for the Item model
    """

    external_id = serializers.CharField(max_length=255, required=True)
    name = serializers.CharField(max_length=255, default="", required=False)
    value = serializers.IntegerField(default=0, required=False)
