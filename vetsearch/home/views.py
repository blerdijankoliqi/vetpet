from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from wagtail.core.models import Page
from .models import LocalityPage, Localities, Clinic
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics
import base64
import json
import requests
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from django.utils.text import slugify
from .serializers import LocalitiesSerializers, ClinicSerializers
from django.contrib.postgres.search import TrigramSimilarity

from django.db.models import Q
from rest_framework.filters import SearchFilter


class LocalitiesAll(generics.ListCreateAPIView):
    queryset = Localities.objects.all()
    serializer_class = LocalitiesSerializers
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["id", "id_from_api", "slug", "postal_code", "postalslug", "country_code", "lat", "lng", "google_places_id", "search_description", "seo_title"]
    search_fields = ['city']
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        city = self.request.query_params.get('city', None)

        if city is not None:
            queryset = queryset.filter(city__icontains=city)

        return queryset


class LocalitiesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Localities.objects.all()
    serializer_class = LocalitiesSerializers
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated]

class ClinicAll(generics.ListCreateAPIView):
    queryset = Clinic.objects.all()
    serializer_class = ClinicSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["id","id_from_api","name","lat","lng","btm_number","phone_number","google_places_id","email","website","pipedrive_id","opening_hours","slug","last_updated_time","pims_type","branch","address","logo","meta_title","meta_description"]
    permission_classes = [IsAuthenticated]


class ClinicDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Clinic.objects.all()
    serializer_class = ClinicSerializers
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated]


def unique_slug_generator(base_slug):
    counter = 1
    slug = base_slug
    while Localities.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
    return slug

def replace_german_letters(string):
    replacements = {
        "ä": "ae",
        "ö": "oe",
        "ß": "ss",
        "ü": "ue",
        "æ": "ae",
        "ø": "oe",
        "å": "aa",
        "é": "e",
        "è": "e"
    }
    for letter, replacement in replacements.items():
        string = string.replace(letter, replacement)
    return string

def convert_json(request):

    response_API = requests.get('https://api-development.petleo.de/v1/localities/')
    data = response_API.text
    parse_json = json.loads(data)

    converted = []
    id = 1
    for item in parse_json:
        converted.append({
            "id": id,
            "id_from_api": item["id"],
            "city": item["city"],
            "postal_code": item["postal_code"],
            "country_code": item["country_code"],
            "lat": item["lat"],
            "lng": item["lng"],
            "google_places_id": item["google_places_id"]
        })
        id += 1
        for sub_locality in item["sub_localities"]:
            converted.append({
                "id": id,
                "id_from_api": item["id"],
                "city": sub_locality,
                "postal_code": item["postal_code"],
                "country_code": item["country_code"],
                "lat": item["lat"],
                "lng": item["lng"],
                "google_places_id": item["google_places_id"]
            })
            id += 1

    for page in converted:
        clean_city = replace_german_letters(page['city'])
        page_slug = unique_slug_generator(slugify(clean_city))
        page_postalslug = f"{page['postal_code']}-{page_slug}"

        locality, created = Localities.objects.get_or_create(
            id_from_api=page['id_from_api'],
            city=page['city'],
            defaults={
                "slug": page_slug,
                "postalslug": page_postalslug,
                "postal_code": page['postal_code'],
                "country_code": page['country_code'],
                "lat": page['lat'],
                "lng": page['lng'],
                "google_places_id": page['google_places_id'],
                "search_description": "Benötigen Sie einen Tierarzt in " + page['city'] + " oder in Ihrer Nähe? Suchen Sie nicht länger. Mit Petleo Vet Search können Sie bequem und schnell den passenden Tierarzt in " + page['city'] + " finden und schnell online Termin buchen.",
                "seo_title": page['city'] + " Tierarztpraxis & Tierarzt in der Nähe | Tierarzttermine einfach online buchen"
            }
        )

        if not created:
            # If the object already exists, update the other fields without overriding search_description and seo_title
            locality.slug = page_slug
            locality.postalslug = page_postalslug
            locality.postal_code = page['postal_code']
            locality.country_code = page['country_code']
            locality.lat = page['lat']
            locality.lng = page['lng']
            locality.google_places_id = page['google_places_id']
            locality.save()

    return HttpResponse("adding")


def convert_and_save_all_clinics(self):
    api_url = "http://api-development.petleo.de/v1/appointment-management/clinics/get_paginated/"
    page = 1
    has_next = True
    username = "karim.abdo@petleo.net"
    password = "p4ssw0rd"
    auth_string = f'{username}:{password}'
    auth_base64 = base64.b64encode(auth_string.encode()).decode()
    headers = {
        'Authorization': f'Basic {auth_base64}',
    }

    while has_next:
        # Fetch the current page from the API
        response = requests.get(f'{api_url}?page={page}', headers=headers)
        input_json = response.json()

        for clinic_data in input_json["results"]:
            # Define the fields that should be updated
            update_fields = {
                "id_from_api": clinic_data["id"],
                "name": clinic_data["name"],
                "lat": clinic_data["lat"],
                "lng": clinic_data["lng"],
                "btm_number": clinic_data["btm_number"],
                "phone_number": clinic_data["phone_number"],
                "google_places_id": clinic_data["google_places_id"],
                "email": clinic_data["email"],
                "website": clinic_data["website"],
                "pipedrive_id": clinic_data["pipedrive_id"],
                "opening_hours": clinic_data["opening_hours"],
                "slug": clinic_data["slug"],
                "last_updated_time": clinic_data["last_updated_time"],
                "pims_type": clinic_data["pims_type"],
                "branch": clinic_data["branch"],
                "address": clinic_data["address"],
                "logo": clinic_data["logo"],
            }

            clinics = Clinic.objects.filter(id_from_api=clinic_data["id"])

            if not clinics:
                # The object doesn't exist, include the meta_description field for creation
                update_fields["meta_description"] = "Vereinbaren Sie online einen Termin mit " + (clinic_data["name"] or "Tierarzt") + " ➤ Öffnungszeiten ✓ Telefonnummer ✉ Adresse"
                update_fields["meta_title"] = "Termin " + (clinic_data["name"] or "Tierarzt")

                # Create the object with the provided fields
                clinic = Clinic.objects.create(**update_fields)
                clinic.save()
            elif len(clinics) == 1:
                clinic = clinics.first()
                # The object exists, update only the specified fields
                for field, value in update_fields.items():
                    setattr(clinic, field, value)
                clinic.save()
            else:
                # Handle the case when multiple objects are returned
                # Update only the specified fields (without meta_title and meta_description)
                for clinic in clinics:
                    for field, value in update_fields.items():
                        setattr(clinic, field, value)
                    clinic.save()

        # Check if there is a next page
        has_next = input_json["next"] is not None

        # Move to the next page
        page += 1

    return JsonResponse({"message": "All clinics saved successfully."}, status=201)



