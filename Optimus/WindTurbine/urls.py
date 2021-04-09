from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('blade', views.blade),
    path('show',views.show),
    path('edit/<int:id>', views.edit),
    path('update/<int:id>', views.update),
    path('delete/<int:id>', views.destroy),

    path('<str:component>', views.detail_view, name='component'),
]