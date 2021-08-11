from django.urls import path

from api import views

urlpatterns = [
    path("geo/", views.api_overview, name="overview"),
    path("geo/geo-list/", views.geo_list, name="geo-list"),
    path("geo/geo-create/", views.geo_create, name="geo-create"),
    path("geo/geo-detail/<int:pk>/", views.geo_detail, name="geo-detail"),
    path("geo/geo-update/<int:pk>/", views.geo_update, name="geo-update"),
    path("geo/geo-delete/<int:pk>/", views.geo_delete, name="geo-delete"),
]
