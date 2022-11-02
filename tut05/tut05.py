import pandas as pd
import numpy as np
import math

from datetime import datetime
start_time = datetime.now()

def average(defi):
    try:
        # Calculating Average Values
        u_avrg = defi['U'].mean()
        v_avrg = defi['V'].mean()
        w_avrg = defi['W'].mean()

        # Calculating Average Value of U, V, W
        defi.insert(4, column="U avrg", value="")
        defi.insert(5, column="V avrg", value="")
        defi.insert(6, column="W avrg", value="")

        defi.at[0, 'U avrg'] = u_avrg
        defi.at[0, 'V avrg'] = v_avrg
        defi.at[0, 'W avrg'] = w_avrg

        # Calculating U', V', W' 
        defi.insert(7, column="U'=U - U avrg", value="")
        defi.insert(8, column="V'=V - V avrg", value="")
        defi.insert(9, column="W'=W - W avrg", value="")

        #for i in range(0,rows):
        defi["U'=U - U avrg"] = defi['U'] - u_avrg
        defi["V'=V - V avrg"] = defi['V'] - v_avrg
        defi["W'=W - W avrg"] = defi['W'] - w_avrg

        return defi
    except:
        print("Error in calculating average.")
        exit()

def insert(defi):
    try:
        #New Octant column being inserted
        defi.insert(10, column="Octant", value="")
        defi.insert(11, column="", value="")

        defi.insert(12, column="Octant ID", value="")
        defi.insert(13, column="1", value="")
        defi.insert(14, column="-1", value="")
        defi.insert(15, column="2", value="")
        defi.insert(16, column="-2", value="")
        defi.insert(17, column="3", value="")
        defi.insert(18, column="-3", value="")
        defi.insert(19, column="4", value="")
        defi.insert(20, column="-4", value="")

        defi.iloc[1, 11] = "User Input"
        defi.at[0, 'Octant ID'] = "Overall Count"
        defi.at[1, 'Octant ID'] = "Mod "+ str(mod) 
        l=[]

        return defi,l
    except:
        print("Error in inserting columns.")
        exit()

def octant(defi,rows,l):
    try:
        # Making the octant value calculations
        for i in range(0, rows):
            if defi.at[i,"U'=U - U avrg"] >= 0 and  defi.at[i,"V'=V - V avrg"] >= 0:
                if defi.at[i,"W'=W - W avrg"] >= 0:
                  defi.at[i, 'Octant'] = 1
                else:
                  defi.at[i, 'Octant'] = -1
            elif defi.at[i,"U'=U - U avrg"] < 0 and  defi.at[i,"V'=V - V avrg"] >= 0:
                if defi.at[i,"W'=W - W avrg"] >= 0:
                  defi.at[i, 'Octant'] = 2
                else:
                  defi.at[i, 'Octant'] = -2
            elif defi.at[i,"U'=U - U avrg"] < 0 and  defi.at[i,"V'=V - V avrg"] < 0:
                if defi.at[i,"W'=W - W avrg"] >= 0:
                  defi.at[i, 'Octant'] = 3
                else:
                  defi.at[i, 'Octant'] = -3
            elif defi.at[i,"U'=U - U avrg"] >= 0 and  defi.at[i,"V'=V - V avrg"] < 0:
                if defi.at[i,"W'=W - W avrg"] >= 0:
                  defi.at[i, 'Octant'] = 4
                else:
                  defi.at[i, 'Octant'] = -4
            l.append(defi.at[i, 'Octant'])

        defi.at[0, "1"] = l.count(1)
        defi.at[0, "-1"] = l.count(-1)
        defi.at[0 ,"2"] = l.count(2)
        defi.at[0 ,"-2"] = l.count(-2)
        defi.at[0 ,"3"] = l.count(3)
        defi.at[0 ,"-3"] = l.count(-3)
        defi.at[0 ,"4"] = l.count(4)
        defi.at[0 ,"-4"] = l.count(-4)

        return defi
    except:
        print("Error in counting octant values.")
        exit()

def split(rows,defi,l):
    try:
        # Find the number of octant values by dividing the list into ranges.
        start = 0
        end = len(l)
        steps = int(mod)
        index=2
        total_rows_mod = math.ceil(rows/steps)
        for i in range(start, end, steps):
            x = i
            sub_list = l[x:x+steps]
            y = x+steps-1
            if y>rows:
                y=rows-1
            defi.at[index ,'Octant ID'] = str(x)+"-"+str(y)
            defi.at[index, '1'] = sub_list.count(1)
            defi.at[index, '-1'] = sub_list.count(-1)
            defi.at[index, '2'] = sub_list.count(2)
            defi.at[index, '-2'] = sub_list.count(-2)
            defi.at[index, '3'] = sub_list.count(3)
            defi.at[index, '-3'] = sub_list.count(-3)
            defi.at[index, '4'] = sub_list.count(4)
            defi.at[index, '-4'] = sub_list.count(-4)
            index+=1

            return defi
    except:
        print("Error in counting octant values for ranges.")
        exit()

def rank_col_inst(defi,octant_name_id_mapping,total_rows_mod):
    try:
        ### Rank Columns insertion 
        column_num = 21
        for i in range(1,5):
            header = "Rank of "+str(i)
            defi.insert(column_num, column=header, value="")
            column_num+=1
            header = "Rank of "+str(-1*i)
            defi.insert(column_num, column=header, value="")
            column_num+=1
        defi.insert(column_num, column="Rank 1 Octant ID", value="")
        column_num+=1
        defi.insert(column_num, column="Rank 1 Octant Name", value="")
        column_num+=1
        
        ### rank for Overall Octant Count calculation
        dict={}
        l=[]
        for i in range(1,5):
            oct_cnt = defi.at[0, str(i)]
            dict[oct_cnt] = str(i)
            l.append(oct_cnt)
            oct_cnt = defi.at[0, str(-1*i)]
            dict[oct_cnt] = str(-1*i)
            l.append(oct_cnt)
        
        l.sort(reverse=True)
        rank = 1
        defi.at[0, "Rank 1 Octant ID"] = dict[l[0]]
        defi.at[0, "Rank 1 Octant Name"] = octant_name_id_mapping[dict[l[0]]]
        
        for i in l:
            octant_id = "Rank of "+dict[i]
            defi.at[0, octant_id] = rank
            rank+=1
        
        ## rank for Mod Octant Count calculation
        rank1=[]
        for index in range(2, total_rows_mod+2): 
            dict={}
            l=[]
            for i in range(1,5):
                oct_cnt = defi.at[index, str(i)]
                dict[oct_cnt] = str(i)
                l.append(oct_cnt)
                oct_cnt = defi.at[index, str(-1*i)]
                dict[oct_cnt] = str(-1*i)
                l.append(oct_cnt)

            l.sort(reverse=True)
            defi.at[index, "Rank 1 Octant ID"] = dict[l[0]]
            rank1.append(dict[l[0]])
            defi.at[index, "Rank 1 Octant Name"] = octant_name_id_mapping[dict[l[0]]]
            
            rank = 1
            for i in l:
                octant_id = "Rank of "+dict[i]
                defi.at[index, octant_id] = rank
                rank+=1
        
        ### Count of Rank 1 Mod Values
        index = total_rows_mod+5
        defi.at[index, '1'] = "Octant ID"
        defi.at[index, '-1'] = "Octant Name"
        defi.at[index, '2'] = "Count of Rank 1 Mod Values"
        index+=1
        for i in range(1,5):
            octant_id = str(i)
            cnt = rank1.count(octant_id)
            defi.at[index, '1'] = octant_id
            defi.at[index, '-1'] = octant_name_id_mapping[octant_id]
            defi.at[index, '2'] = cnt
            index+=1
            
            octant_id = str(-1*i)
            cnt = rank1.count(octant_id)
            defi.at[index, '1'] = octant_id
            defi.at[index, '-1'] = octant_name_id_mapping[octant_id]
            defi.at[index, '2'] = cnt
            index+=1
            
    except Exception as e:
        print("Error in calculating rank.", e)
            
def octant_range_names(mod):
    octant_name_id_mapping = {"1":"Internal outward interaction", "-1":"External outward interaction", "2":"External Ejection", "-2":"Internal Ejection", "3":"External inward interaction", "-3":"Internal inward interaction", "4":"Internal sweep", "-4":"External sweep"}
    
    # Read Excel File
    try:
        defi = pd.read_excel('octant_input.xlsx')
        rows = defi.shape[0]
    except:
        print("Error in reading Excel file.")
        exit()
    
    # Average Values calculation
    defi = average(defi)

    #new columns insertion
    defi,l = insert(defi)

    # the octant values calculation   
    defi= octant(defi,rows,l)

    
    # Divide the list into ranges and count the octant values.
    defi = split(rows,defi)
    
    # Rank calculation
    defi = rank_col_inst(defi,octant_name_id_mapping,rows)
    
 
    try:
        defi.to_excel('octant_output_ranking_excel.xlsx', index=False)
    except:
        print("Error in exporting to CSV.")
        exit()
        
from platform import python_version
ver = python_version()

if ver == "3.8.10":
    print("Correct Version Installed")
else:
    print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")


mod=5000 
octant_range_names(mod)

#This shall be the last lines of the code.
end_time = datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))