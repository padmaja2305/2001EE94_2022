from glob import glob
from platform import python_version
import pandas as pd
import numpy as np
import math

data_frame = None
rows = None
iter = 0

def reading_excel_file(filename):
    global data_frame
    global rows
    try:
        data_frame = pd.read_excel("input_octant_longest_subsequence_with_range.xlsx")
        rows = data_frame.shape[0]
    except Exception as e:
        print(e)
        print("Error: file not found")
        exit(1)

def average():
    global data_frame
    global rows
    try:
        # Calculating Average Values
        u_avg = data_frame['U'].mean()
        v_avg = data_frame['V'].mean()
        w_avg = data_frame['W'].mean()

        # Calculating Average Value of U, V, W
        data_frame.insert(4, column="U Avg", value="")
        data_frame.insert(5, column="V Avg", value="")
        data_frame.insert(6, column="W Avg", value="")

        data_frame.at[0, 'U Avg'] = u_avg
        data_frame.at[0, 'V Avg'] = v_avg
        data_frame.at[0, 'W Avg'] = w_avg

        # Calculating U', V', W'
        data_frame.insert(7, column="U'=U - U avg", value="")
        data_frame.insert(8, column="V'=V - V avg", value="")
        data_frame.insert(9, column="W'=W - W avg", value="")

        # for i in range(0,rows):
        data_frame["U'=U - U avg"] = data_frame['U'] - u_avg
        data_frame["V'=V - V avg"] = data_frame['V'] - v_avg
        data_frame["W'=W - W avg"] = data_frame['W'] - w_avg
    except:
        print("Error in calculating average.")
        exit()

def insert_octant_column():
    try:
        # Inserting new column for Octant
        data_frame.insert(10, column="Octant", value="")
        data_frame.insert(11, column="", value="")

        data_frame.insert(12, column="Octant ID", value="")
        # data_frame.insert(13, column="1", value="")
        # data_frame.insert(14, column="-1", value="")
        # data_frame.insert(15, column="2", value="")
        # data_frame.insert(16, column="-2", value="")
        # data_frame.insert(17, column="3", value="")
        # data_frame.insert(18, column="-3", value="")
        # data_frame.insert(19, column="4", value="")
        # data_frame.insert(20, column="-4", value="")

        data_frame.iloc[1, 11] = "User Input"
        data_frame.at[0, 'Octant ID'] = "Overall Count"
        data_frame.at[1, 'Octant ID'] = "Mod " + str(mod)
    except:
        print("Error in inserting columns.")
        exit()

