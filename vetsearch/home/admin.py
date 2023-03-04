from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    modeladmin_register,
)

from .models import Localities

class LocalitiesAdmin(ModelAdmin):
    model = Localities
    menu_label = "Localities"
    menu_icon = "placeholder"
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("id_from_api", "city", "slug", "postal_code", "country_code", "lat", "lng", "google_places_id", "search_description", "seo_title",)
    search_fields = ("id_from_api", "city", "slug", "postal_code", "country_code", "lat", "lng", "google_places_id", "search_description", "seo_title",)

modeladmin_register(LocalitiesAdmin)
