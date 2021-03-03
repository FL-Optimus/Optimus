from WindTurbine.models import Airfoil
import pandas as pd

def get_properties(airfoil_id):
    try:
        airfoil = Airfoil.objects.get(id = airfoil_id)
    except:
        airfoil = None
    if airfoil:
        df = pd.read_csv('WindTurbine/airfoils/geometry/NACA_2414.csv',
            skiprows=1, delim_whitespace=True, names=['x', 'y'])
        y_values = [float(v) for v in df['y']]
        len_y = len(y_values) if len(y_values)//2 == 0 else len(y_values)+1
        end_value = int(len_y/2)

        airfoil.thickness = 20
        airfoil.thickness_loc = 20
        airfoil.camber = 20
        airfoil.camber_loc = 20
        airfoil.save()
        # print(end_value)

