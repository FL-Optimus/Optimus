import os
import subprocess
import numpy as np
from pathlib import Path

def call_xfoil(airfoilname, a_range, a_step, Res):
    for Re in Res:
        path = Path(f'polars/{airfoilname}/{Re}')
        path.mkdir(parents=True, exist_ok=True)

        with open (path/'input_file.in', 'w') as input_file:
            input_file.write(f"LOAD geometry/{airfoilname}.csv\n")
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
        os.remove(":00.bl")

# call_xfoil('n2414', [0,10], 0.25, 100000)
