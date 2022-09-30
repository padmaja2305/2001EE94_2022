import pandas as pd
import numpy as np
import math

def octact_identification(mod):
    
    try:
        # Reading Excel File
        df = pd.read_excel('input_octant_longest_subsequence.xlsx')
        rows = df.shape[0]
    except:
        print("Error in reading Excel file.")
        exit()
    
    try:
        # Calculating Average Values
        u_avg = df['U'].mean()
        v_avg = df['V'].mean()
        w_avg = df['W'].mean()

        # Calculating Average Value of U, V, W
        df.insert(4, column="U Avg", value="")
        df.insert(5, column="V Avg", value="")
        df.insert(6, column="W Avg", value="")

        df.at[0, 'U Avg'] = u_avg
        df.at[0, 'V Avg'] = v_avg
        df.at[0, 'W Avg'] = w_avg

        # Calculating U', V', W' 
        df.insert(7, column="U'=U - U avg", value="")
        df.insert(8, column="V'=V - V avg", value="")
        df.insert(9, column="W'=W - W avg", value="")

        #for i in range(0,rows):
        df["U'=U - U avg"] = df['U'] - u_avg
        df["V'=V - V avg"] = df['V'] - v_avg
        df["W'=W - W avg"] = df['W'] - w_avg
    except:
        print("Error in calculating average.")
        exit()
        
    try:
        #Inserting new column for Octant
        df.insert(10, column="Octant", value="")
        df.insert(11, column="", value="")

        df.insert(12, column="Octant ID", value="")
        df.insert(13, column="Longest Subsequence Length", value="")
        df.insert(14, column="Count", value="")
        l=[]
        # Calculating the octant values
        for i in range(0, rows):
            if df.at[i,"U'=U - U avg"] >= 0 and  df.at[i,"V'=V - V avg"] >= 0:
                if df.at[i,"W'=W - W avg"] >= 0:
                  df.at[i, 'Octant'] = 1
                else:
                  df.at[i, 'Octant'] = -1
            elif df.at[i,"U'=U - U avg"] < 0 and  df.at[i,"V'=V - V avg"] >= 0:
                if df.at[i,"W'=W - W avg"] >= 0:
                  df.at[i, 'Octant'] = 2
                else:
                  df.at[i, 'Octant'] = -2
            elif df.at[i,"U'=U - U avg"] < 0 and  df.at[i,"V'=V - V avg"] < 0:
                if df.at[i,"W'=W - W avg"] >= 0:
                  df.at[i, 'Octant'] = 3
                else:
                  df.at[i, 'Octant'] = -3
            elif df.at[i,"U'=U - U avg"] >= 0 and  df.at[i,"V'=V - V avg"] < 0:
                if df.at[i,"W'=W - W avg"] >= 0:
                  df.at[i, 'Octant'] = 4
                else:
                  df.at[i, 'Octant'] = -4
            l.append(df.at[i, 'Octant'])
    except:
        print("Error in calculating Octant values.")
        exit()
        
    try:
        #-------- Tutorial 3 - Longest Sequence ---------------

        ### Dataframe to store longest sequence and Count
        data=[]
        df2 = pd.DataFrame(data, index=['1','-1','2','-2','3','-3','4','-4'],
                       columns=['Len', 'Count'])
        df2 = df2.fillna(0)
        prev = df.at[0, 'Octant'] 
        df2.at[str(prev), 'Len'] = 1
        cur_len = 1
        for idx in range(1,rows):
            cur = df.at[idx, 'Octant']
            if (cur == prev):
                cur_len+=1
            else:
                cur_len = 1

            if (cur_len == df2.at[str(cur), 'Len']):
                df2.at[str(cur), 'Count'] += 1
            elif(cur_len > df2.at[str(cur), 'Len']):
                df2.at[str(cur), 'Count'] = 1

            df2.at[str(cur), 'Len'] = max(cur_len, df2.at[str(cur), 'Len'])
            prev = cur
        #print(df2)

        ### Inserting values in dataframe
        idx = 0
        for i in range(1,5):
            df.at[idx, 'Octant ID'] = str(i)
            df.at[idx, 'Longest Subsequence Length'] = df2.at[str(i), 'Len']
            df.at[idx, 'Count'] = df2.at[str(i), 'Count']
            idx+=1
            df.at[idx, 'Octant ID'] = str(-1*i)
            df.at[idx, 'Longest Subsequence Length'] = df2.at[str(-1*i), 'Len']
            df.at[idx, 'Count'] = df2.at[str(-1*i), 'Count']
            idx+=1
    except:
        print("Error in calculating longest sequence.")
        exit()
    
    try:
        ### Exporting dataframe to excel
        df.to_excel('output_octant_longest_subsequence.xlsx', index=False)
    except:
        print("Error in exporting to Excel file.")
        exit()
        
from platform import python_version
ver = python_version()

if ver == "3.8.10":
    print("Correct Version Installed")
else:
    print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")
  
mod = 7000
octact_identification(mod)
