from django.shortcuts import render
from django.http import HttpResponse
from wagtail.core.models import Page
from .models import LocalityPage
from django.core.exceptions import ObjectDoesNotExist

import json
import requests

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
    for page in converted:
        
        ind = 0
        try:
            page = Page.objects.get(title=page['city'])
            ind=1

        except ObjectDoesNotExist:
            ind=2

        if ind==2:
            parent_page = Page.objects.get(title='Localities')
            print(parent_page.slug)
            locality_page = LocalityPage(
                title=page['city'],
                id_from_api=page['id_from_api'],
                city=page['city'],
                postal_code=page['postal_code'],
                country_code=page['country_code'],
                lat=page['lat'],
                lng=page['lng'],
                google_places_id=page['google_places_id'],
                search_description="Benötigen Sie einen Tierarzt in " + page['city'] + " oder in Ihrer Nähe? Suchen Sie nicht länger. Mit Petleo Vet Search können Sie bequem und schnell den passenden Tierarzt in " + page['city'] + " finden und schnell online Termin buchen.",
                seo_title=page['city'] + " Tierarztpraxis & Tierarzt in der Nähe | Tierarzttermine einfach online buchen"
            )
            parent_page.add_child(instance=locality_page)
            locality_page.save()            
    
    return HttpResponse("adding")

