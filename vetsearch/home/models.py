from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from django.template.defaultfilters import slugify
from django.utils.text import get_valid_filename

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
    
class Localities(models.Model):
        id_from_api = models.IntegerField()
        city = models.CharField(max_length=255, null=True, blank=True)
        slug = models.CharField(max_length=255, null=True, blank=True)
        postal_code = models.CharField(max_length=20, null=True, blank=True)
        postalslug = models.CharField(max_length=510, null=True, blank=True)
        country_code = models.CharField(max_length=10, null=True, blank=True)
        lat = models.CharField(max_length=255, null=True, blank=True)
        lng = models.CharField(max_length=255, null=True, blank=True)
        google_places_id = models.CharField(max_length=255, null=True, blank=True)
        search_description = models.CharField(max_length=500, null=True, blank=True)
        seo_title = models.CharField(max_length=255, null=True, blank=True)
        search_description_en = models.CharField(max_length=500, null=True, blank=True)
        seo_title_en = models.CharField(max_length=255, null=True, blank=True)


        def __str__(self):
             return self.city


class Clinic(models.Model):
    id_from_api = models.IntegerField()
    name = models.CharField(max_length=255, null=True, blank=True, default="Tierarzt")
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)
    btm_number = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    google_places_id = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    website = models.URLField(max_length=255, null=True, blank=True)
    pipedrive_id = models.IntegerField(null=True, blank=True)
    opening_hours = models.TextField(null=True, blank=True)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    last_updated_time = models.DateTimeField(null=True, blank=True)
    pims_type = models.CharField(max_length=255, null=True, blank=True)
    branch = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True)
    logo = models.URLField(max_length=255, null=True, blank=True)
    meta_title = models.CharField(max_length=255, null=True, blank=True)
    meta_description = models.CharField(max_length=500, null=True, blank=True)
    meta_title_en = models.CharField(max_length=255, null=True, blank=True)
    meta_description_en = models.CharField(max_length=500, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Create a slug if it's not provided
        if not self.slug:
            self.slug = slugify(self.name)

        # Check for slug uniqueness
        slug = self.slug
        counter = 1
        while Clinic.objects.filter(slug=slug).exclude(id=self.id).exists():
            slug = f"{self.slug}-{counter}"
            counter += 1

        self.slug = slug

        # Save the object
        super(Clinic, self).save(*args, **kwargs)

    def __str__(self):
        return self.name





