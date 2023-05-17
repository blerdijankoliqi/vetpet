from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    modeladmin_register,
)

from .models import Localities, Clinic

class LocalitiesAdmin(ModelAdmin):
    model = Localities
    menu_label = "Localities"
    menu_icon = "placeholder"
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("id_from_api", "city", "slug", "postal_code", "country_code", "lat", "lng", "google_places_id", "search_description", "seo_title", "search_description_en", "seo_title_en",)
    search_fields = ("id_from_api", "city", "slug", "postal_code", "country_code", "lat", "lng", "google_places_id", "search_description", "seo_title", "search_description_en", "seo_title_en",)

modeladmin_register(LocalitiesAdmin)

class ClinicAdmin(ModelAdmin):
    model = Clinic
    menu_label = "Clinic"
    menu_icon = "placeholder"
    menu_order = 291
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("id","name","meta_title","meta_description", "meta_title_en","meta_description_en",)
    search_fields = ("id","id_from_api","name","lat","lng","btm_number","phone_number","google_places_id","email","website","pipedrive_id","opening_hours","slug","last_updated_time","pims_type","branch","address","logo","meta_title","meta_description", "meta_title_en","meta_description_en",)

modeladmin_register(ClinicAdmin)
