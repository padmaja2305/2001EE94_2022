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

    #Inserting new column for Octant
    df.insert(10, column="Octant", value="")
    df.insert(11, column="", value="")
    df.insert(12, column="Octant ID", value="")
    df.insert(13, column="1", value="")
    df.insert(14, column="-1", value="")
    df.insert(15, column="2", value="")
    df.insert(16, column="-2", value="")
    df.insert(17, column="3", value="")
    df.insert(18, column="-3", value="")
    df.insert(19, column="4", value="")
    df.insert(20, column="-4", value="")

    df.iloc[1, 11] = "User Input"
    df['Octant ID'][0] = "Overall Count"
    df['Octant ID'][1] = "Mod "+mod 
    l=[]

# Calculating the octant values
    for i in range(0, rows):
      if df["U'=U - U avg"][i] >= 0 and  df["V'=V - V avg"][i] >= 0:
        if df["W'=W - W avg"][i] >= 0:
          df['Octant'][i] = 1
        else:
          df['Octant'][i] = -1
      elif df["U'=U - U avg"][i] < 0 and  df["V'=V - V avg"][i] >= 0:
        if df["W'=W - W avg"][i] >= 0:
          df['Octant'][i] = 2
        else:
          df['Octant'][i] = -2
      elif df["U'=U - U avg"][i] < 0 and  df["V'=V - V avg"][i] < 0:
        if df["W'=W - W avg"][i] >= 0:
          df['Octant'][i] = 3
        else:
          df['Octant'][i] = -3
      elif df["U'=U - U avg"][i] >= 0 and  df["V'=V - V avg"][i] < 0:
        if df["W'=W - W avg"][i] >= 0:
          df['Octant'][i] = 4
        else:
          df['Octant'][i] = -4
      l.append(df['Octant'][i])

    df["1"][0] = l.count(1)
    df["-1"][0] = l.count(-1)
    df["2"][0] = l.count(2)
    df["-2"][0] = l.count(-2)
    df["3"][0] = l.count(3)
    df["-3"][0] = l.count(-3)
    df["4"][0] = l.count(4)
    df["-4"][0] = l.count(-4)