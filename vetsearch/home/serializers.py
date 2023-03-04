from rest_framework import serializers
from .models import Localities

class LocalitiesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Localities
        fields = (
            "id",
            "id_from_api",
            "city",
            "slug",
            "postal_code",
            "country_code",
            "lat",
            "lng",
            "google_places_id",
            "search_description",
            "seo_title",
        )