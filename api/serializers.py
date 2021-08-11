from rest_framework import serializers

from api.models import GEO


class GEOSerializer(serializers.ModelSerializer):
    class Meta:
        model = GEO
        fields = ["id", "address", "longitude", "latitude", "created_at"]
        read_only_fields = ["longitude", "latitude"]
