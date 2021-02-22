from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('customers/', views.render_pdf_view, name='customers'),
]
