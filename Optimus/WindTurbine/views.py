from django.shortcuts import render

from django.http import HttpResponse
from django.template.loader import get_template

from .models import Airfoil

# Create your views here.
def home(request):
    return render(request, 'index.html')

def airfoil_detail_view(request, id):
    try:
        airfoil = Airfoil.objects.get(id=id)
    except Airfoil.DoesNotExist:
        return render(request, '404.html')

    context = {
        'airfoil': airfoil
    }

    return render(request, 'airfoil_detail.html', context)
