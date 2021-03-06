from django.shortcuts import render

from django.http import HttpResponse
from django.template.loader import get_template

from .airfoils.aerodynamics import get_properties
from .models import Airfoil

# Create your views here.
def home(request):
    return render(request, 'index.html')

def airfoil_list_view(request):
    try:
        airfoils = Airfoil.objects.all()[:10]
    except Airfoil.DoesNotExist:
        return render(request, '404.html')
    context = {
        'airfoils': airfoils
    }

    return render(request, 'airfoil_list.html', context)

def get_airfoil_properties(airfoil):
    try:
        x = airfoil.geometry['x']
        y = airfoil.geometry['y']
    except TypeError:
        return None

    end_value = int(round(len(x)/2))

    thickness = [abs(y[i]) + abs(y[-1-i]) for i,j in enumerate(x[:end_value])]
    camber = [(y[i] + y[-1-i])/2 for i, j in enumerate(x[:end_value])]

    max_thickness = max(thickness)
    max_thickness_position = x[thickness.index(max_thickness)] * 100

    max_camber = max(camber)
    max_camber_position = x[camber.index(max_camber)] * 100

    properties = {
        'thickness': f'{max_thickness * 100 :.2f}',
        'thickness_position': f'{max_thickness_position :.2f}',
        'camber': f'{max_camber * 100 :.2f}',
        'camber_position':  f'{max_camber_position :.2f}',
    }
    return properties


def airfoil_detail_view(request, id):
    try:
        airfoil = Airfoil.objects.get(id=id)
    except Airfoil.DoesNotExist:
        airfoil = get_properties(airfoil.id)
    except:
        return render(request, '404.html')
    if airfoil.thickness and airfoil.camber:
        thickness = airfoil.thickness
        camber = airfoil.camber
        properties = [thickness, camber]
    else:
        properties = get_airfoil_properties(airfoil)
    context = {
        'airfoil': airfoil,
        'properties': properties,
    }

    return render(request, 'airfoil_detail.html', context)
