import pandas as pd
import numpy as np
import math
pd.options.mode.chained_assignment = None

def octact_identification(mod):
    # Reading CSV File
    df = pd.read_csv('octant_input.csv')
    rows = df.shape[0]

    # Calculating Average Values
    u_average = df['U'].mean()
    v_average = df['V'].mean()
    w_average = df['W'].mean()

    # Calculating Average Value of U, V, W
    df.insert(4, column="U Avg", value="")
    df.insert(5, column="V Avg", value="")
    df.insert(6, column="W Avg", value="")

    df['U Avg'][0] = u_avg
    df['V Avg'][0] = v_avg
    df['W Avg'][0] = w_avg
        
    # Calculating Average Values
    u_average = df['U'].mean()
    v_average = df['V'].mean()
    w_average = df['W'].mean()

    # Calculating U', V', W' 
    df.insert(7, column="U'=U - U average", value="")
    df.insert(8, column="V'=V - V average", value="")
    df.insert(9, column="W'=W - W average", value="")
    
    #for i in range(0,rows):
    df["U'=U - U average"] = df['U'] - u_average
    df["V'=V - V average"] = df['V'] - v_average
    df["W'=W - W average"] = df['W'] - w_average