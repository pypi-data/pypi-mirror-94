import numpy as np
import pandas as pd



def read_matlab_magnet(test_number):
    file_name = f'test{test_number}.magnet'
    df = pd.read_csv(file_name, delim_whitespace=True)
    design = [list(df[key]) for key in list(df)]
    return design

def read_matlab_field(test_number):
    file_name = f'test{test_number}.field'
    df = pd.read_csv(file_name, delim_whitespace=True)
    first_col = list(df[list(df)[0]])
    z_d = first_col.count(first_col[0])
    r_d = int(len(first_col) / z_d)
    return [np.reshape(np.array(df[label]), (r_d, z_d), order='F') for label in
            ['r(mm)', 'z(mm)', 'Br(T)', 'Bz(T)']]

def read_matlab_inductance(test_number):
    file_name = f'test{test_number}.inductance'
    df = pd.read_csv(file_name, delim_whitespace=True)
    return df.to_numpy()