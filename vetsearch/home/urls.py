from django.urls import path
from . import views

urlpatterns = [  
    path('reload', views.convert_json),  # app homepage
    path("localities/", views.LocalitiesAll.as_view()),
    path("localities/<str:slug>/", views.LocalitiesDetail.as_view()),
] 