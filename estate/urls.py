from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("signup/", views.signup,name ="signup"),
    path("", views.property_list, name="property_list"),
    path("properties/<int:pk>/", views.property_detail, name="property_detail"),
    path("properties/create/", views.property_create, name="property_create"),
    path("properties/<int:pk>/edit/", views.property_update, name="property_update"),
    path("properties/<int:pk>/delete/", views.property_delete, name="property_delete"),
]
