from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel

from wagtail.api import APIField

class HomePage(Page):
    max_count = 1
    subpage_types = ['home.SubPage']
    pass

class SubPage(Page):
    max_count = 2
    subpage_types = ['home.LocalityPage']
    pass

class LocalityPage(Page):
    subpage_types = []

    id_from_api = models.IntegerField()
    city = models.CharField(max_length=255, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    country_code = models.CharField(max_length=10, null=True, blank=True)
    lat = models.CharField(max_length=255, null=True, blank=True)
    lng = models.CharField(max_length=255, null=True, blank=True)
    google_places_id = models.CharField(max_length=255, null=True, blank=True)

    api_fields = [
        APIField("id_from_api"),
        APIField("city"),
        APIField("postal_code"),
        APIField("country_code"),
        APIField("lat"),
        APIField("lng"),
        APIField("google_places_id"),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('id_from_api'),
        FieldPanel('city'),
        FieldPanel('postal_code'),
        FieldPanel('country_code'),
        FieldPanel('lat'),
        FieldPanel('lng'),
        FieldPanel('google_places_id'),
    ]

    def get_locality_subpages(self):
        return self.get_children().type(LocalityPage).live()
