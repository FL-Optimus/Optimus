import pandas as pd
import numpy as np
# import matplotlib as mpl
# mpl.use('TkAgg') 
# import matplotlib
# matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

def test():
    df = pd.read_csv('geometry/n2414.csv', names=['x', 'y'])
    reference_x = list(np.linspace(1, 0, num=180)) + list(np.linspace(0, 1, num=180))
    # print((reference_x))
    plt.plot(df['x'], df['y'])
    plt.show()

test()
