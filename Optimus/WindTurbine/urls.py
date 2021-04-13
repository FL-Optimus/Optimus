from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('materials', views.materials_view, name='materials'),
    # path('materials/<name>', views.material_detail_view, name='materials'),
]