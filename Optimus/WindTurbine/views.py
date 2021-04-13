from django.shortcuts import render
from .models import Material
# Create your views here.
def home(request):
    return render(request, 'index.html')

def materials_view(request):
    materials = Material.objects.all()

    context = {
        'materials': materials
    }
    return render(request, 'materials.html', context)

# def material_detail_view(request, name):
#     try:
#         material = Material.objects.get(name=name)
#     except Material.DoesNotExist:
#         material = None
#     context = {
#         'material': material
#     }
#     return render(request, 'material.html', context)