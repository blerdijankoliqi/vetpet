from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from wagtail.core.models import Page
from .models import LocalityPage, Localities, Clinic
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics
import base64
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated




import json
import requests

from .models import Localities
from .serializers import LocalitiesSerializers, ClinicSerializers


class LocalitiesAll(generics.ListCreateAPIView):
    queryset = Localities.objects.all()
    serializer_class = LocalitiesSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["id", "id_from_api", "city", "slug", "postal_code", "country_code", "lat", "lng", "google_places_id", "search_description", "seo_title"]
    permission_classes = [IsAuthenticated]


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
        locality, created = Localities.objects.get_or_create(
            id_from_api=page['id_from_api'],
            city=page['city'],
            defaults={
                "slug": page['city'].lower(),
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
            locality.slug = page['city'].lower()
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

            try:
                # Check if the object already exists in the database
                clinic = Clinic.objects.get(id_from_api=clinic_data["id"])
            except Clinic.DoesNotExist:
                # The object doesn't exist, include the meta_description field for creation
                update_fields["meta_description"] = "Vereinbaren Sie online einen Termin mit " + (clinic_data["name"] or "Tierarzt") + " ➤ Öffnungszeiten ✓ Telefonnummer ✉ Adresse"
                update_fields["meta-title"] = "Termin " + (clinic_data["name"] or "Tierarzt")


                # Create the object with the provided fields
                clinic = Clinic.objects.create(id_from_api=clinic_data["id"], **update_fields)
                clinic.save()
            else:
                # The object exists, update only the specified fields
                for field, value in update_fields.items():
                    setattr(clinic, field, value)
                clinic.save()

        # Check if there is a next page
        has_next = input_json["next"] is not None

        # Move to the next page
        page += 1

    return JsonResponse({"message": "All clinics saved successfully."}, status=201)

