import numpy as np
import h5py
import os

matrix1 = np.random.random(size=(1000,1000))
matrix2 = np.random.random(size=(1000,1000))
matrix3 = np.random.random(size=(1000,1000))
matrix4 = np.random.random(size=(1000,1000))


def check_duplicates(overwrite_file):
     while overwrite_file != 'y' or overwrite_file != 'n':
            overwrite_file = input("Do you want to overwrite it? [y/n] ")

            if overwrite_file.lower() == 'n':
                return False
            elif overwrite_file.lower() != 'y':
                print('Input was not "y" or "n", please try again.')
            else:
                return True


def create_hdf5_dataset(filename):
    if os.path.isfile(filename):
        overwrite_file = None
        print(f"File {filename} already exist.")
        overwrite_file = check_duplicates(overwrite_file)
        if overwrite_file == True:
            with h5py.File(filename, 'w') as hdf:
                hdf.create_dataset('dataset1', data=matrix1)
                hdf.create_dataset('dataset2', data=matrix2)


def create_hdf5_group(filename):
    with h5py.File(filename, 'w') as hdf:
        G1 = hdf.create_group('Group1')
        G1.create_dataset('dataset1', data=matrix1, compression='gzip', compression_opts=9)
        G1.create_dataset('dataset4', data=matrix4, compression='gzip', compression_opts=9)

        G21 = hdf.create_group('Group2/Subgroup1')
        G21.create_dataset('dataset3', data=matrix3, compression='gzip', compression_opts=9)

        G22 = hdf.create_group('Group2/Subgroup2')
        G22.create_dataset('dataset2', data=matrix2, compression='gzip', compression_opts=9)

create_hdf5_dataset('hdf5_testfile.h5')
# create_hdf5_group('hdf5_testfile.h5')

def read_from_hdf(filename):
    files_not_found = []
    try:
        with h5py.File(filename, 'r') as hdf:
            main_groups = list(hdf.keys())
            for group in main_groups:
                print(group)
                sub_groups = list(hdf.get(group))
                for subgroup in sub_groups:
                    print('---',subgroup)

    except FileNotFoundError:
        files = os.listdir()
        for file in files:
            if file.endswith('.h5'):
                files_not_found.append(file)
        print(f'File {filename} could not be found. Did you mean one of the following?')
        for file_not_found in files_not_found:
            print('- ', file_not_found)
# read_from_hdf('hdf5_testfile.h5')