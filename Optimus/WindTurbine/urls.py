from django.urls import path

from . import views
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = [
    path('', views.home, name='home'),
    path('generators', views.generator_list_view, name='generators'),
    path('generators/<gen_type>', views.generator_detail_view, name='generator_types'),
]

# urlpatterns += staticfiles_urlpatterns()
