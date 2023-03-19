from django.urls import path
from . import views

urlpatterns = [  
    path('reload', views.convert_json),  # app homepage
    path('clinics-reload', views.convert_and_save_all_clinics), 
    path("localities/", views.LocalitiesAll.as_view()),
    path("localities/<str:slug>/", views.LocalitiesDetail.as_view()),
    path("clinics/", views.ClinicAll.as_view()),
    path("clinics/<str:slug>/", views.ClinicDetail.as_view()),
] 