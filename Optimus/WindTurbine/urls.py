from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('airfoils', views.airfoil_list_view, name='airfoils'),
    path('airfoils/<int:id>', views.airfoil_detail_view, name='airfoil_detail'),
]