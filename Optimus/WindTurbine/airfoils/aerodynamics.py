from os import walk
from WindTurbine.models import Airfoil

from ..apis import apis

import pandas as pd
import requests
import csv
import json
import numpy as np

def read_airfoil_csv(airfoil):
    df = pd.read_csv(f'WindTurbine/airfoils/geometry/{airfoil.name}.csv', names=['x', 'y'])
    return df

def read_polar_csv(airfoil):
    try:
        df = pd.read_csv(f'WindTurbine/airfoils/polars/{airfoil.name}/100000/{airfoil.name}.csv', skiprows=10, delim_whitespace=True)
        df = df[1:]   
        df['alpha'] = df['alpha'].astype(float)
        df['CL'] = df['CL'].astype(float)
        return df 
    except:
        return None

def read_folder(path):
    a, airfoils, b = next(walk(path))
    print(a, airfoils, b)


def get_airfoil_from_api(request, airfoilname):
    data = None
    api = apis['airfoils']

    response = requests.get(api['url'] + airfoilname + api['extension'] )
    if response.status_code == 200:
        data = response.text

    return data


def read_airfoil_from_db(id):
    airfoil = Airfoil.objects.get(id=id)
    df = pd.read_json(airfoil.geometry)
    read_folder('WindTurbine/airfoils/geometry')

    return

def organize_airfoil_data(geometry):
    if geometry[0][0] == 1:
        geometry = geometry
    else:
        limit = int(len(geometry)/2)
        first_part = geometry[:limit]
        first_part = first_part[::-1]
        second_part = geometry[limit:]
        geometry = first_part + second_part

    return geometry


def save_as_csv(airfoilname, geometry):
    with open(f'WindTurbine/airfoils/geometry/{airfoilname}.csv', 'w') as f:
        writer = csv.writer(f)
        for row in geometry:
            writer.writerow((f'{row[0]:.5f}', f'{row[1]:.5f}'))

def save_to_db(airfoilname, geometry):
    x_values = [value[0] for value in geometry]
    y_values = [value[1] for value in geometry]
    geo2json = json.dumps({"x":x_values, "y":y_values})
    if Airfoil.objects.filter(name=airfoilname):
        return
    airfoil = Airfoil(name=airfoilname, geometry=geo2json, polar=None)
    airfoil.save()

def create_circular_airfoil():
    x_list = [np.sin(np.radians(i))*0.5+0.5 for i in range(0,361,6)]
    y_list = [np.cos(np.radians(i))*0.5 for i in range(0,361,6)]    

    geometry = list(zip(x_list, y_list))
    new_x = [0.5 + x * np.cos(np.radians(-90)) - y * np.sin(np.radians(-90)) for x, y in geometry]
    new_y = [-0.5 + x * np.sin(np.radians(90)) + y * np.cos(np.radians(-90)) for x, y in geometry]    
    geometry = list(zip(new_x, new_y))

    save_as_csv('Circular', geometry)
    save_to_db('Circular', geometry)

import subprocess
import os
from pathlib import Path
def call_xfoil(id, a_range, a_step, Res):
    airfoilname = Airfoil.objects.get(id=id).name
    for Re in Res:

        path = Path(f'WindTurbine/airfoils/polars/{airfoilname}/{Re}')
        path.mkdir(parents=True, exist_ok=True)

        with open (path/'input_file.in', 'w') as input_file:
            # input_file.write("PLOP\n")
            # input_file.write("G\n\n")
            input_file.write(f"LOAD WindTurbine/airfoils/geometry/{airfoilname}.csv\n")
            input_file.write(airfoilname + '\n')
            input_file.write("PANE\n")
            input_file.write("OPER\n")
            input_file.write(f"Visc {Re}\n")
            input_file.write("PACC\n")
            input_file.write(f"{path}/{airfoilname}.csv\n\n")
            input_file.write("ITER 200\n")
            input_file.write(f"ASeq {a_range[0]} {a_range[1]} {a_step}\n")
            input_file.write("\n\n")
            input_file.write("quit\n")

        subprocess.call(f"xfoil < {path}/input_file.in", shell=True)
        if os.path.exists(f"{path}/input_file.in"):
            os.remove(f"{path}/input_file.in")
        try:
            os.remove(":00.bl")
        except:
            pass


# def airfoil_polars(path, airfoil, Re):
#     df = pd.read_csv(f'{path}/{airfoil}/{Re}', skiprows=10, delim_whitespace=True)
#     df = df[1:]
#     alpha = df['alpha']
#     cL = df['CL']
#     cD = df['CD']
#     L2D = [float(cl)/float(cd) for cl, cd in zip(cL, cD)]
#     max_L2D, max_position = max(L2D), L2D.index(max(L2D))
#     polars = {
#         'alpha': alpha[max_position],
#         'L2D': max_L2D
#     }
#     return polars

# def collect_Res(path, airfoil):
#     _, _, Re = next(walk(path+f'/{airfoil}'))
#     Re = {}
#     for value in Re:
#         if value:
#             Re.update({value.strup('.csv') : airfoil_polars(path, airfoil, value)})
#     return Re

# def collect_airfoils(path):
#     _, airfoils, _ = next(walk(path))
#     airfoil = {}
#     for name in airfoils:
#         if name:
#             airfoil[name] = {'Re': collect_Res(path, name)}
#     return airfoil

# aero = collect_airfoils('airfoils/geometry')