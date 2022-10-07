import pandas as pd
import numpy as np

pd.options.mode.chained_assignment = None

    #defining average value
def average (df):
    u_average = df['U'].mean()
    v_average = df['V'].mean()
    w_average = df['W'].mean()
    return u_average,v_average,w_average


def octact_identification(mod):
    # Reading CSV File
    df = pd.read_csv('octant_input.csv')
    rows = df.shape[0]

    # Calculating Avg Value of U, V, W
    df.insert(4, column="U average", value="")
    df.insert(5, column="V average", value="")
    df.insert(6, column="W average", value="")

    df['U average'][0], df['V average'][0], df['W average'][0]= average(df)
        
    # Calculating Avg Values
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

    df.iloc[1, 11] = "User Input"  #df.add is better way to access
    df['Octant ID'][0] = "Overall Count"  #df.at [row, header] is better way to access
    df['Octant ID'][1] = "Mod "+mod 
    l=[]

# Calculating the octant values
    for i in range(0, rows):
      if df["U'=U - U average"][i] >= 0 and  df["V'=V - V average"][i] >= 0:
        if df["W'=W - W average"][i] >= 0:
          df['Octant'][i] = 1
        else:
          df['Octant'][i] = -1
      elif df["U'=U - U average"][i] < 0 and  df["V'=V - V average"][i] >= 0:
        if df["W'=W - W average"][i] >= 0:
          df['Octant'][i] = 2
        else:
          df['Octant'][i] = -2
      elif df["U'=U - U average"][i] < 0 and  df["V'=V - V average"][i] < 0:
        if df["W'=W - W average"][i] >= 0:
          df['Octant'][i] = 3
        else:
          df['Octant'][i] = -3
      elif df["U'=U - U average"][i] >= 0 and  df["V'=V - V average"][i] < 0:
        if df["W'=W - W average"][i] >= 0:
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

    # Split list into ranges and finding the count of octant values
    start = 0
    end = len(l)
    step = int(mod)
    idx=2
    for i in range(start, end, step):
        x = i
        sub_list = l[x:x+step]
        #print(sub_list)
        y = x+step-1
        if y >= rows:
            y = rows-1
        df['Octant ID'][idx] = str(x)+"-"+str(y)
        df['1'][idx] = sub_list.count(1)
        df['-1'][idx] = sub_list.count(-1)
        df['2'][idx] = sub_list.count(2)
        df['-2'][idx] = sub_list.count(-2)
        df['3'][idx] = sub_list.count(3)
        df['-3'][idx] = sub_list.count(-3)
        df['4'][idx] = sub_list.count(4)
        df['-4'][idx] = sub_list.count(-4)
        idx+=1

    #print(df)
    df.to_csv('octant_output.csv', index=False)


mod= input("Enter MOD:\n")
octact_identification(mod)