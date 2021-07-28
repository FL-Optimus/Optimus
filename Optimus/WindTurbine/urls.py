from django.urls import path

from . import views
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = [
    path('', views.home, name='home'),
    path('airfoils', views.airfoil_list_view, name='airfoils'),
    path('airfoils/<int:id>', views.airfoil_detail_view, name='airfoil_detail'),
    path('airfoils/circular', views.airfoil_circular_view, name='add circular airfoil'),
    path('airfoils/<int:id>/calculate', views.airfoil_calculate_view, name='arun xfoil on airfoil'),

    path('airfoils/<int:id>/read', views.airfoil_read_view, name='get airfoil polars'),

    path('airfoils/pdf', views.render_pdf_view, name='test-view'),
    path('airfoils/<int:id>/pdf', views.render_pdf_view, name='test-view'),
    path('airfoils/<str:airfoilname>', views.airfoil_add_view, name='add airfoil'),
    path('airfoils/<int:id>/delete', views.airfoil_delete_view, name='airfoil_detail'),

    path('airfoils/read/<str:airfoilname>', views.get_airfoil_from_api, name='read from db'),
    path('generators', views.generator_list_view, name='generators'),
    path('generators/<gen_type>', views.generator_detail_view, name='generator_types'),

]
