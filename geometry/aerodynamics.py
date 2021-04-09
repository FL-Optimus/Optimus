import os
from os import walk
# from WindTurbine.models import Airfoil

import pandas as pd

# def get_properties(airfoil_id):
#     try:
#         airfoil = Airfoil.objects.get(id = airfoil_id)
#     except:
#         airfoil = None
#     if airfoil:
#         df = pd.read_csv('WindTurbine/airfoils/geometry/NACA_2414.csv',
#             delim_whitespace=True)
#         df.columns = ['x', 'y']
#         x_values = [x for x in df['x']]
#         y_values = [y for y in df['y']]
#         is_even = len(y_values)//2 == 0

#         end_value = int(len(y_values)/2) if is_even else int((len(y_values)+1)/2)

#         abs_y = [abs(y) for y in y_values if y != 0]

#         thickness = [abs_y[i] + abs_y[-i-1] for i in range(len(abs_y))]
#         thickness = thickness[:end_value]
#         max_thickness = max(thickness)
#         thickness_loc = x_values[thickness.index(max_thickness)]

#         camber = [(y_values[i] + y_values[-i-1])/2 for i in range(len(y_values))]
#         camber = camber[:end_value]
#         max_camber = max(camber)
#         camber_loc = x_values[camber.index(max_camber)]

#         airfoil.thickness = f'{max_thickness*100:.2f}'
#         airfoil.thickness_loc = f'{thickness_loc*100:.2f}'
#         airfoil.camber = f'{max_camber*100:.2f}'
#         airfoil.camber_loc = f'{camber_loc*100:.2f}'
#         airfoil.save()
#     return airfoil


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
#     _, _, Res = next(walk(path+f'/{airfoil}'))
#     Re = {}
#     for value in Res:
#         if value:
#             Re.update({value.strip('.csv') : airfoil_polars(path, airfoil, value)})
#     return Re

# def get_new_properties(path, airfoil):
    # not_read = []
    # try:
    #     df = pd.read_csv(f'{path}/{airfoil}', delim_whitespace=True, skiprows=1)
    #     # df.dropna()
    #     # print(df)
    #     df.columns=['x', 'y']
    # except:
    #     not_read.append(airfoil)
    # not_starting_with_1 = []
    # if df['x'][0] != 1:
    #     try:
    #         df = pd.read_csv(f'{path}/{airfoil}', delim_whitespace=True)
    #         df.columns=['x', 'y']
    #     except:
    #         not_starting_with_1.append(airfoil)
    # if airfoil in not_read or airfoil in not_starting_with_1:
    #     return None

def read_special_airfoils(path, airfoil, df):
    first_part = df[:int(len(df)/2)]
    second_part = df[int(len(df)/2):]

    swapped_part = first_part[::-1].reset_index(drop=True)

    df = pd.concat([swapped_part, second_part])
    return df


def get_properties(path, airfoil):
    df = pd.read_csv(f'{path}/{airfoil}', delim_whitespace=True, names=['x', 'y'], skiprows=1)
    try:
        if float(df['x'][0]) > 1:
            df = pd.read_csv(f'{path}/{airfoil}', delim_whitespace=True, names=['x', 'y'], skiprows=2)
    except:
        pass

    if 'GOE' in airfoil or 'FX' in airfoil or 'RG' in airfoil:
        df = read_special_airfoils(path, airfoil, df)
    try:
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

        properties = {
            'thickness': max_thickness,
            'thickness_loc': thickness_loc,
            'camber': max_camber,
            'camber_loc': camber_loc,
        }
    except:
        properties = {
            'thickness': None,
            'thickness_loc': None,
            'camber': None,
            'camber_loc': None,
        }

    geom = pd.DataFrame([[x_values[i], y_values[i]] for i in range(len(df))], columns=['x', 'y'])
    geom.to_csv(f'geometry/out/{airfoil}', index=False, float_format='%.5f')
    return properties

def collect_airfoils(path):
    airfoils = {}
    for airfoil in os.listdir(path):
        airfoils[airfoil] = {'properties': get_properties(path, airfoil)}

    return airfoils

aero = collect_airfoils('./geometry/in')
for key, values in aero.items():
    print(key, values)

# cities = pd.DataFrame([['Sacramento', 'California'], ['Miami', 'Florida']], columns=['City', 'State'])
# cities.to_csv('cities.csv')