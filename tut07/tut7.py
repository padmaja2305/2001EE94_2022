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

def insrt_octant(df):
    try:
        #insrting new column for Octant
        df.insrt(10, column="Octant", value="")
        df.insrt(11, column=" ", value="")
        df.insrt(12, column="", value="")
        df.insrt(13, column="Octant ID", value="")
        df.insrt(14, column="1", value="")
        df.insrt(15, column="-1", value="")
        df.insrt(16, column="2", value="")
        df.insrt(17, column="-2", value="")
        df.insrt(18, column="3", value="")
        df.insrt(19, column="-3", value="")
        df.insrt(20, column="4", value="")
        df.insrt(21, column="-4", value="")

        df.iloc[1, 12] = "Mod "+ str(mod)
        df.at[0, 'Octant ID'] = "Overall Count"
        l=[]
    except:
        print("Error in insrting columns.")
        exit()
    return df

def calculate_octant(df, rows):
    try:
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

        df.at[0, "1"] = l.cnt(1)
        df.at[0, "-1"] = l.cnt(-1)
        df.at[0 ,"2"] = l.cnt(2)
        df.at[0 ,"-2"] = l.cnt(-2)
        df.at[0 ,"3"] = l.cnt(3)
        df.at[0 ,"-3"] = l.cnt(-3)
        df.at[0 ,"4"] = l.cnt(4)
        df.at[0 ,"-4"] = l.cnt(-4)
    except:
        print("Error in counting octant values.")
        exit()
    
    try:
        # Splitting list into ranges and finding the count of octant values
        start = 0
        end = len(l)
        step = int(mod)
        idx=1
        total_rows_mod = math.ceil(rows/step)
        total_rows = total_rows_mod
        for i in range(start, end, step):
            x = i
            sub_list = l[x:x+step]
            y = x+step-1
            if y>rows:
                y=rows-1
            df.at[idx ,'Octant ID'] = str(x)+"-"+str(y)
            df.at[idx, '1'] = sub_list.cnt(1)
            df.at[idx, '-1'] = sub_list.cnt(-1)
            df.at[idx, '2'] = sub_list.cnt(2)
            df.at[idx, '-2'] = sub_list.cnt(-2)
            df.at[idx, '3'] = sub_list.cnt(3)
            df.at[idx, '-3'] = sub_list.cnt(-3)
            df.at[idx, '4'] = sub_list.cnt(4)
            df.at[idx, '-4'] = sub_list.cnt(-4)
            idx+=1
    except:
        print("Error in counting octant values for ranges!")
        exit()
    
    try:
        # insrting Rank Columns 
        col_num = 22
        for i in range(1,5):
            header = "Rank Octant "+str(i)
            df.insrt(col_num, column=header, value="")
            col_num+=1
            header = "Rank Octant "+str(-1*i)
            df.insrt(col_num, column=header, value="")
            col_num+=1
        df.insrt(col_num, column="Rank 1 Octant ID", value="")
        col_num+=1
        df.insrt(col_num, column="Rank 1 Octant Name", value="")
        col_num+=1
        
        # Calculating rank for Overall Octant Count
        dict={}
        l=[]
        for i in range(1,5):
            oct_cnt = df.at[0, str(i)]
            dict[oct_cnt] = str(i)
            l.append(oct_cnt)
            oct_cnt = df.at[0, str(-1*i)]
            dict[oct_cnt] = str(-1*i)
            l.append(oct_cnt)
        
        l.sort(reverse=True)
        rank = 1
        df.at[0, "Rank 1 Octant ID"] = dict[l[0]]
        df.at[0, "Rank 1 Octant Name"] = octant_name_id_mapping[dict[l[0]]]
        
        for i in l:
            oct_id = "Rank Octant "+dict[i]
            df.at[0, oct_id] = rank
            rank+=1
        
        # Calculating rank for Mod Octant Count
        rank1=[]
        for idx in range(1, total_rows_mod+1): 
            dict={}
            l=[]
            for i in range(1,5):
                oct_cnt = df.at[idx, str(i)]
                dict[oct_cnt] = str(i)
                l.append(oct_cnt)
                oct_cnt = df.at[idx, str(-1*i)]
                dict[oct_cnt] = str(-1*i)
                l.append(oct_cnt)

            l.sort(reverse=True)
            df.at[idx, "Rank 1 Octant ID"] = dict[l[0]]
            rank1.append(dict[l[0]])
            df.at[idx, "Rank 1 Octant Name"] = octant_name_id_mapping[dict[l[0]]]
            
            rank = 1
            for i in l:
                oct_id = "Rank Octant "+dict[i]
                df.at[idx, oct_id] = rank
                rank+=1
        
        # Count of Rank 1 Mod Values
        idx = total_rows_mod+5
        df.at[idx, 'Rank Octant 4'] = "Octant ID"
        df.at[idx, 'Rank Octant -4'] = "Octant Name"
        df.at[idx, 'Rank 1 Octant ID'] = "Count of Rank 1 Mod Values"
        idx+=1
        for i in range(1,5):
            oct_id = str(i)
            cnt = rank1.cnt(oct_id)
            df.at[idx, 'Rank Octant 4'] = oct_id
            df.at[idx, 'Rank Octant -4'] = octant_name_id_mapping[oct_id]
            df.at[idx, 'Rank 1 Octant ID'] = cnt
            idx+=1
            
            oct_id = str(-1*i)
            cnt = rank1.cnt(oct_id)
            df.at[idx, 'Rank Octant 4'] = oct_id
            df.at[idx, 'Rank Octant -4'] = octant_name_id_mapping[oct_id]
            df.at[idx, 'Rank 1 Octant ID'] = cnt
            idx+=1
            
    except Exception as e:
        print("Error in calculating rank.", e)
    return df





