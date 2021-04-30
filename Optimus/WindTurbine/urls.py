from django.urls import path

from . import views
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = [
    path('', views.home, name='home'),
    path('airfoils', views.airfoil_list_view, name='airfoils'),
    path('airfoils/<int:id>', views.airfoil_detail_view, name='airfoil_detail'),
    path('generators', views.generator_list_view, name='generators'),
    path('generators/<gen_type>', views.generator_detail_view, name='generator_types'),
]
