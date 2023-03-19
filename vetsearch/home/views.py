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


def convert_json(self):
    
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



    # Works
    # for page in converted:
        
    #     ind = 0
    #     try:
    #         page = Page.objects.get(title=page['city'])
    #         ind=1

    #     except ObjectDoesNotExist:
    #         ind=2

    #     if ind==2:
    #         parent_page = Page.objects.get(title='Localities')
    #         print(parent_page.slug)
    #         locality_page = LocalityPage(
    #             title=page['city'],
    #             id_from_api=page['id_from_api'],
    #             city=page['city'],
    #             postal_code=page['postal_code'],
    #             country_code=page['country_code'],
    #             lat=page['lat'],
    #             lng=page['lng'],
    #             google_places_id=page['google_places_id'],
    #             search_description="Benötigen Sie einen Tierarzt in " + page['city'] + " oder in Ihrer Nähe? Suchen Sie nicht länger. Mit Petleo Vet Search können Sie bequem und schnell den passenden Tierarzt in " + page['city'] + " finden und schnell online Termin buchen.",
    #             seo_title=page['city'] + " Tierarztpraxis & Tierarzt in der Nähe | Tierarzttermine einfach online buchen"
    #         )
    #         parent_page.add_child(instance=locality_page)
    #         locality_page.save()  




    for page in converted:
        ind=0

        try:
            page = Localities.objects.get(city=page['city'])

        except Localities.DoesNotExist:
            ind = 1
        
        if ind == 1:
            locality_page = Localities(
                id_from_api=page['id_from_api'],
                city=page['city'],
                slug=page['city'].lower(),
                postal_code=page['postal_code'],
                country_code=page['country_code'],
                lat=page['lat'],
                lng=page['lng'],
                google_places_id=page['google_places_id'],
                search_description="Benötigen Sie einen Tierarzt in " + page['city'] + " oder in Ihrer Nähe? Suchen Sie nicht länger. Mit Petleo Vet Search können Sie bequem und schnell den passenden Tierarzt in " + page['city'] + " finden und schnell online Termin buchen.",
                seo_title=page['city'] + " Tierarztpraxis & Tierarzt in der Nähe | Tierarzttermine einfach online buchen"
            )
            locality_page.save() 
                      
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

        for clinic in input_json["results"]:
            if clinic["name"] == None:
                new_clinic = {
                    "id":clinic["id"],
                    "id_from_api": clinic["id"],
                    "name": clinic["name"],
                    "lat": clinic["lat"],
                    "lng": clinic["lng"],
                    "btm_number": clinic["btm_number"],
                    "phone_number": clinic["phone_number"],
                    "google_places_id": clinic["google_places_id"],
                    "email": clinic["email"],
                    "website": clinic["website"],
                    "pipedrive_id": clinic["pipedrive_id"],
                    "opening_hours": clinic["opening_hours"],
                    "slug": clinic["slug"],
                    "last_updated_time": clinic["last_updated_time"],
                    "pims_type": clinic["pims_type"],
                    "branch": clinic["branch"],
                    "address": clinic["address"],
                    "logo": clinic["logo"],
                    "meta_title": "Termin Tierarzt",
                    "meta_description": "Vereinbaren Sie online einen Termin mit Tierarzt ➤ Öffnungszeiten ✓ Telefonnummer ✉ Adresse"
                }
                # Save clinic to the database
                Clinic.objects.update_or_create(
                    id=new_clinic["id"],
                    defaults=new_clinic
                )

            else:
                new_clinic = {
                    "id":clinic["id"],
                    "id_from_api": clinic["id"],
                    "name": clinic["name"],
                    "lat": clinic["lat"],
                    "lng": clinic["lng"],
                    "btm_number": clinic["btm_number"],
                    "phone_number": clinic["phone_number"],
                    "google_places_id": clinic["google_places_id"],
                    "email": clinic["email"],
                    "website": clinic["website"],
                    "pipedrive_id": clinic["pipedrive_id"],
                    "opening_hours": clinic["opening_hours"],
                    "slug": clinic["slug"],
                    "last_updated_time": clinic["last_updated_time"],
                    "pims_type": clinic["pims_type"],
                    "branch": clinic["branch"],
                    "address": clinic["address"],
                    "logo": clinic["logo"],
                    "meta_title": "Termin " + clinic["name"],
                    "meta_description": "Vereinbaren Sie online einen Termin mit " + clinic["name"] + " ➤ Öffnungszeiten ✓ Telefonnummer ✉ Adresse"
                }
                # Save clinic to the database
                Clinic.objects.update_or_create(
                    id=new_clinic["id"],
                    defaults=new_clinic
                )


        # Check if there is a next page
        has_next = input_json["next"] is not None

        # Move to the next page
        page += 1

    return JsonResponse({"message": "All clinics saved successfully."}, status=201)

