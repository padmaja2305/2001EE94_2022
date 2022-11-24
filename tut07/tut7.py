# imports

import os
import pandas as pd
import numpy as np
import math
import openpyxl as xl
from openpyxl.styles import PatternFill, Border, Side, Alignment, Font, fills
from datetime import datetime
from platform import python_version

ver = python_version()
start_time = datetime.now()
octant_name_id_mapping = {"1":"Internal outward interaction", "-1":"External outward interaction", "2":"External Ejection", "-2":"Internal Ejection", "3":"External inward interaction", "-3":"Internal inward interaction", "4":"Internal sweep", "-4":"External sweep"}


def rdfile(filename):
    try:
        df = pd.read_excel(f'input/{filename}')
        rows = df.shape[0]
    except Exception as e:
        print("Error in reading Excel file!", e)
        exit()
    return df, rows

def avarage(df):
    try:
        # Calculating avg Values
        u_avg = df['U'].mean()
        v_avg = df['V'].mean()
        w_avg = df['W'].mean()

        # Calculating Average Value of U, V, W
        df.insrt(4, column="U Avg", value="")
        df.insrt(5, column="V Avg", value="")
        df.insrt(6, column="W Avg", value="")

        # Calculating U', V', W' 
        df.insrt(7, column="U'=U - U avg", value="")
        df.insrt(8, column="V'=V - V avg", value="")
        df.insrt(9, column="W'=W - W avg", value="")

        df["U'=U - U avg"] = round(df['U'] - u_avg, 3)
        df["V'=V - V avg"] = round(df['V'] - v_avg, 3)
        df["W'=W - W avg"] = round(df['W'] - w_avg , 3)
        
        df.at[0, 'U Avg'] = round(u_avg, 3)
        df.at[0, 'V Avg'] = round(v_avg, 3)
        df.at[0, 'W Avg'] = round(w_avg, 3)
        
        df['U'] = round(df['U'], 3)
        df['V'] = round(df['V'], 3)
        df['W'] = round(df['W'], 3)
        df['T'] = round(df['T'], 3)
    except:
        print("Error in calculating average!")
        exit()
    return df





