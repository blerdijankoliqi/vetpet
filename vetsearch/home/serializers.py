from rest_framework import serializers
from .models import Localities, Clinic

class LocalitiesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Localities
        fields = (
            "id",
            "id_from_api",
            "city",
            "slug",
            "postal_code",
            "postalslug",
            "country_code",
            "lat",
            "lng",
            "google_places_id",
            "search_description",
            "seo_title",
            "search_description_en",
            "seo_title_en",
        )

class ClinicSerializers(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        fields = ("id","id_from_api","name","lat","lng","btm_number","phone_number","google_places_id","email","website","pipedrive_id","opening_hours","slug","last_updated_time","pims_type","branch","address","logo","meta_title","meta_description", "meta_title_en","meta_description_en",)