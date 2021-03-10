from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('generators', views.generator_list_view, name='generators'),
]