import csv
import pandas as pd
import requests 

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import get_template
from json import dumps

from .airfoils.aerodynamics import (
    read_airfoil_csv, 
    get_airfoil_from_api, 
    organize_airfoil_data,
    call_xfoil,
    read_polar_csv, 
    save_as_csv, 
    save_to_db,
    create_circular_airfoil)
from .apis import apis
from .models import Airfoil, Material
from .forms import ContactForm
from .utils import get_plot, get_form

# Create your views here.
def home(request):
    return render(request, 'index.html')

def generator_list_view(request):
    types = [f'Type{i}' for i in range(1,5)]
    context = {
        'types': types
    }
    return render(request, 'components/generator/generator.html', context)


def generator_detail_view(request, gen_type):
    print(f'components/generator/types/{gen_type}.html')
    # types/{gen_type}

    return render(request, f'components/generator/types/{gen_type}.html')


def airfoil_list_view(request):
    try:
        airfoils = Airfoil.objects.all()[:10]
    except Airfoil.DoesNotExist:
        return render(request, '404.html')
    search = None
    data = None
    circular = False
    form = get_form(request)
    if form.is_valid():
        airfoilname = form.cleaned_data['name']
        data = get_airfoil_from_api(request, airfoilname)
    if data:
        search = airfoilname
    airfoilnames = [airfoil.name for airfoil in airfoils]

    if 'Circular' in airfoilnames:
        circular = True

    context = {
        'form': form,
        'airfoils': airfoils,
        'search': search,
        'circular': circular
    }

    return render(request, 'airfoil_list.html', context)

def airfoil_add_view(request, airfoilname):
    airfoildata = get_airfoil_from_api(request, airfoilname)
    airfoildata = airfoildata.split()
    header = []
    geometry = []
    for row in airfoildata:
        try:
            if -2 < float(row) < 2:
                geometry.append(float(row))
        except:
            header.append(row)
        
    airfoildata = list(zip(geometry[0::2], geometry[1::2]))
    geometry = organize_airfoil_data(airfoildata)
    save_as_csv(airfoilname, geometry)
    save_to_db(airfoilname, geometry)
    return redirect('airfoils')

def airfoil_detail_view(request, id):
    try:
        airfoil = Airfoil.objects.get(id=id)
    except Airfoil.DoesNotExist:
        airfoil = None

    if not airfoil:
        return render(request, '404.html')

    geo = read_airfoil_csv(airfoil)
    polars = read_polar_csv(airfoil)
    polar_chart = []
    if isinstance(polars, pd.DataFrame):
        polar_chart = {'name': 'polars', 'chart': get_plot(polars['alpha'], polars['CL'], 'Polars', ['alpha', 'cL'])}
    
    charts = [
        {'name': 'geometry', 'chart': get_plot(geo['x'], geo['y'], 'Geometry', ['x', 'y'], y_lim=(-0.55, 0.55))},
        polar_chart,
    ]

    context = {
        'charts': charts,
        'airfoil': airfoil,
    }

    return render(request, 'airfoil_detail.html', context)

def airfoil_calculate_view(request, id):
    call_xfoil(id, [-20,20], 0.1, [100000, 500000, 1000000])
    return redirect ('airfoils')

import matplotlib.pyplot as plt
def airfoil_read_view(request, id):
    airfoil = Airfoil.objects.get(id=id)
    df = pd.read_csv(f'WindTurbine/airfoils/polars/{airfoil.name}/100000/{airfoil.name}.csv', skiprows=10, delim_whitespace=True)
    df = df[1:]
    # print(df)
    plt.plot(df['alpha'], df['CL'])
    plt.show()

    return redirect ('airfoils')

def airfoil_circular_view(request):
    create_circular_airfoil()
    return redirect('airfoils')

def airfoil_delete_view(request, id):
    try:
        airfoil = Airfoil.objects.get(id=id)
    except airfoil.DoesNotExist:
        airfoil = None
    if airfoil:
        airfoil.delete()
    return redirect('airfoils')



# def plots_view(request):

#     geo = read_airfoil_csv()
#     # plots = read_polars_csv()
#     x = [1,2,3,4]#geo['x']
#     y = [5,3,6,4]#geo['y']

#     # chart = get_plot(x, y)
#     charts = [
#         {'name': 'chart1', 'chart': get_plot(geo['x'], geo['y'], 'Geometry', ['x', 'y'])},
#         {'name': 'chart2', 'chart': get_plot(x, y, 'Something Else', ['x', 'y'])},
#     ]

#     airfoil = None
#     form = get_form(request)
#     if form.is_valid():
#         airfoil = form.cleaned_data['name']

#     context = {
#         'charts': charts,
#         'form': form,
#         'airfoil': airfoil
#     }
#     return render(request, 'plots.html', {'context': context})



# def get_airfoil_from_api(request, airfoilname):
#     data = None
#     api = apis['airfoils']

#     response = requests.get(api['url'] + airfoilname + api['extension'] )

#     if response.status_code == 200:
#         data = response.text
#         print('DATA', data)
#         data = data.split()
#     else:
#         context = {
#             'error': f'Airfoil {airfoilname} not found'
#         }
#         return render(request, 'airfoil_list.html', {'context':context})


#     return redirect('airfoils')



from django.http import HttpResponse
from django.template.loader import get_template 
from xhtml2pdf import pisa

def render_pdf_view(request, *args, **kwargs):
    try:
        title = Airfoil.objects.get(id=kwargs['id'])
    except KeyError:
        title = 'Document Title'
    template_path = 'testpdf.html'
    context = {'myvar': 'this is your template context', 'title': title, 'logo': ''}
    
    response = HttpResponse(content_type='application/pdf')
    # if download:
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # if display:
    response['Content-Disposition'] = ' filename="report.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response