from os import walk
from WindTurbine.models import Airfoil

import pandas as pd

def get_properties(airfoil_id):
    try:
        airfoil = Airfoil.objects.get(id = airfoil_id)
    except:
        airfoil = None
    if airfoil:
        df = pd.read_csv('WindTurbine/airfoils/geometry/NACA_2414.csv',
            delim_whitespace=True)
        df.columns = ['x', 'y']
        x_values = [x for x in df['x']]
        y_values = [y for y in df['y']]
        is_even = len(y_values)//2 == 0

        end_value = int(len(y_values)/2) if is_even else int((len(y_values)+1)/2)

        abs_y = [abs(y) for y in y_values if y != 0]

        thickness = [abs_y[i] + abs_y[-i-1] for i in range(len(abs_y))]
        thickness = thickness[:end_value]
        max_thickness = max(thickness)
        thickness_loc = x_values[thickness.index(max_thickness)]

        camber = [(y_values[i] + y_values[-i-1])/2 for i in range(len(y_values))]
        camber = camber[:end_value]
        max_camber = max(camber)
        camber_loc = x_values[camber.index(max_camber)]

        airfoil.thickness = f'{max_thickness*100:.2f}'
        airfoil.thickness_loc = f'{thickness_loc*100:.2f}'
        airfoil.camber = f'{max_camber*100:.2f}'
        airfoil.camber_loc = f'{camber_loc*100:.2f}'
        airfoil.save()
    return airfoil


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