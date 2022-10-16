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

def insert_octant_values():
    global data_frame
    l = []
    try:
        # Calculating the octant values
        for i in range(0, rows):
            if data_frame.at[i, "U'=U - U avg"] >= 0 and data_frame.at[i, "V'=V - V avg"] >= 0:
                if data_frame.at[i, "W'=W - W avg"] >= 0:
                    data_frame.at[i, 'Octant'] = 1
                else:
                    data_frame.at[i, 'Octant'] = -1
            elif data_frame.at[i, "U'=U - U avg"] < 0 and data_frame.at[i, "V'=V - V avg"] >= 0:
                if data_frame.at[i, "W'=W - W avg"] >= 0:
                    data_frame.at[i, 'Octant'] = 2
                else:
                    data_frame.at[i, 'Octant'] = -2
            elif data_frame.at[i, "U'=U - U avg"] < 0 and data_frame.at[i, "V'=V - V avg"] < 0:
                if data_frame.at[i, "W'=W - W avg"] >= 0:
                    data_frame.at[i, 'Octant'] = 3
                else:
                    data_frame.at[i, 'Octant'] = -3
            elif data_frame.at[i, "U'=U - U avg"] >= 0 and data_frame.at[i, "V'=V - V avg"] < 0:
                if data_frame.at[i, "W'=W - W avg"] >= 0:
                    data_frame.at[i, 'Octant'] = 4
                else:
                    data_frame.at[i, 'Octant'] = -4
            l.append(data_frame.at[i, 'Octant'])

        # data_frame.at[0, "1"] = l.count(1)
        # data_frame.at[0, "-1"] = l.count(-1)
        # data_frame.at[0, "2"] = l.count(2)
        # data_frame.at[0, "-2"] = l.count(-2)
        # data_frame.at[0, "3"] = l.count(3)
        # data_frame.at[0, "-3"] = l.count(-3)
        # data_frame.at[0, "4"] = l.count(4)
        # data_frame.at[0, "-4"] = l.count(-4)
        return l
    except:
        print("Error in counting octant values.")
        exit()

def count_ocatant_value(l): 
    global data_frame
    global iter
    try:
        # Split list into ranges and find the count of octant values
        start = 0
        end = len(l)
        step = int(mod)
        iter = 2
        total_rows_mod = math.ceil(rows/step)
        for i in range(start, end, step):
            x = i
            sub_list = l[x:x+step]
            y = x+step-1
            if y > rows:
                y = rows-1
            data_frame.at[iter, 'Octant ID'] = str(x)+"-"+str(y)
            data_frame.at[iter, '1'] = sub_list.count(1)
            data_frame.at[iter, '-1'] = sub_list.count(-1)
            data_frame.at[iter, '2'] = sub_list.count(2)
            data_frame.at[iter, '-2'] = sub_list.count(-2)
            data_frame.at[iter, '3'] = sub_list.count(3)
            data_frame.at[iter, '-3'] = sub_list.count(-3)
            data_frame.at[iter, '4'] = sub_list.count(4)
            data_frame.at[iter, '-4'] = sub_list.count(-4)
            iter += 1

        # Verified Column
        data_frame.at[iter, 'Octant ID'] = "Verified"
        for i in range(-4, 5):
            if i == 0:
                continue
            data_frame.at[iter, str(i)] = data_frame[str(
                i)].iloc[2:(2+total_rows_mod)].sum()
    except:
        print("Error in counting octant values for ranges.")
        exit()

def transistion_count():
    global data_frame
    global iter
    try:
        # -------------- Overall Transition Count ----------------------

        iter += 3
        data_frame.at[iter, 'Octant ID'] = "Overall Transition Count"
        iter += 1
        data_frame.at[iter, '1'] = 'To'
        iter += 1
        data_frame.at[iter, 'Octant ID'] = 'Count'
        for k in range(-4, 5):
            if k == 0:
                continue
            data_frame.at[iter, str(k)] = k
        iter += 1
        data_frame.at[iter, ''] = "From"

        # Creating dataframe to store values
        matrix = []
        data_frame2 = pd.DataFrame(matrix, index=['1', '-1', '2', '-2', '3', '-3', '4', '-4'],
                                   columns=['1', '-1', '2', '-2', '3', '-3', '4', '-4'])

        data_frame2 = data_frame2.fillna(0)

        # Calculating values
        for i in range(0, rows-1):
            first = str(data_frame.at[i, 'Octant'])
            second = str(data_frame.at[i+1, 'Octant'])
            data_frame2.at[first, second] += 1

        # Adding values to main dataframe
        for k in range(1, 5):
            data_frame.at[iter, 'Octant ID'] = str(k)
            for l in range(-4, 5):
                if l == 0:
                    continue
                data_frame.at[iter, str(l)] = data_frame2.at[str(k), str(l)]
            iter += 1
            data_frame.at[iter, 'Octant ID'] = str(-1*k)
            for l in range(-4, 5):
                if l == 0:
                    continue
                data_frame.at[iter, str(l)] = data_frame2.at[str(-1*k), str(l)]
            iter += 1
    except:
        print("Error in calculating Overall Transition Count.")
        exit()

def mod_transiston(mod):
    global data_frame
    global iter
    step = int(mod)
    try:
        # ------------ Mod Transition Count ------------------
        for i in range(0, rows, step-1):
            lim = i+step-1
            if lim >= rows:
                lim = rows-1
            iter += 2
            data_frame.at[iter, 'Octant ID'] = 'Mod Transition Count'
            iter += 1
            data_frame.at[iter, 'Octant ID'] = str(i)+'-'+str(lim)
            data_frame.at[iter, '1'] = 'To'
            iter += 1
            data_frame.at[iter, 'Octant ID'] = 'Count'
            for k in range(-4, 5):
                if k == 0:
                    continue
                data_frame.at[iter, str(k)] = k
            iter += 1
            data_frame.at[iter, ''] = "From"

            # Creating dataframe to store values
            matrix = []
            data_frame2 = pd.DataFrame(matrix, index=['1', '-1', '2', '-2', '3', '-3', '4', '-4'],
                                       columns=['1', '-1', '2', '-2', '3', '-3', '4', '-4'])
            data_frame2 = data_frame2.fillna(0)

            # Calculating values
            for j in range(i, lim):
                first = str(data_frame.at[j, 'Octant'])
                second = str(data_frame.at[j+1, 'Octant'])
                data_frame2.at[first, second] += 1

            # Adding values to main dataframe
            for k in range(1, 5):
                data_frame.at[iter, 'Octant ID'] = str(k)
                for l in range(-4, 5):
                    if l == 0:
                        continue
                    data_frame.at[iter, str(l)] = data_frame2.at[str(k), str(l)]
                iter += 1
                data_frame.at[iter, 'Octant ID'] = str(-1*k)
                for l in range(-4, 5):
                    if l == 0:
                        continue
                    data_frame.at[iter, str(
                        l)] = data_frame2.at[str(-1*k), str(l)]
                iter += 1
    except:
        print("Error in calculating Mod Transition Count.")
        exit()

def writing_excel_file(filename):
    try:
        # Exporting dataframe to excel
        data_frame.to_excel(
            filename, index=False)
    except:
        print("Error in exporting to excel.")
        exit()
matrix=[]
def setup():

    temp_df = pd.DataFrame(matrix, index=['1','-1','2','-2','3','-3','4','-4'],
    columns=['Len', 'Count'])
    temp_df = temp_df.fillna(0)

    return temp_df



def octact_identification(mod):
    global data_frame
    reading_excel_file("input_octant_longest_subsequence_with_range.xlsx")
    average()
    insert_octant_column()
    l = insert_octant_values()
    # count_ocatant_value(l)
    # transistion_count()
    # mod_transiston(mod)
    try:

        temp_df = setup()
        
        temp_df_1 = pd.DataFrame(matrix, columns=['1','-1','2','-2','3','-3','4','-4'])

        bpr = data_frame.at[0, 'Octant'] 
        temp_df.at[str(bpr), 'Len'] = 1

        lent = 1
        beg = data_frame.at[0,'Time']
        searchf = data_frame.at[0, 'Time']
        for iter in range(1,rows):
            pres = data_frame.at[iter, 'Octant']
            if (pres == bpr):
                lent+=1
            else:
                lent = 1
                beg = data_frame.at[iter, 'Time']
            searchf = data_frame.at[iter, 'Time']
            temp_data_frame2 = temp_df_1.count(axis=0)
            if (lent == temp_df.at[str(pres), 'Len']):
                temp_df.at[str(pres), 'Count'] += 1                
                temp_df_1.at[temp_data_frame2[str(pres)], str(pres)] = beg
                temp_df_1.at[temp_data_frame2[str(pres)]+1, str(pres)] = searchf
            elif(lent > temp_df.at[str(pres), 'Len']):
                temp_df.at[str(pres), 'Count'] = 1
                del temp_df_1[str(pres)]
                temp_df_1.insert(7, column = str(pres), value="")
                temp_df_1.at[0, str(pres)] = beg
                temp_df_1.at[1, str(pres)] = searchf
            temp_df_1.replace('', np.nan, inplace=True)
            temp_df.at[str(pres), 'Len'] = max(lent, temp_df.at[str(pres), 'Len'])
            bpr = pres

        iter = 0
        for i in range(1,5):
            data_frame.at[iter, 'Octant ID'] = str(i)
            data_frame.at[iter, 'Longest Subsequence Length'] = temp_df.at[str(i), 'Len']
            
            data_frame.at[iter, 'Count'] = temp_df.at[str(i), 'Count']
            iter+=1
            data_frame.at[iter, 'Octant ID'] = str(-1*i)
            data_frame.at[iter, 'Longest Subsequence Length'] = temp_df.at[str(-1*i), 'Len']
            
            data_frame.at[iter, 'Count'] = temp_df.at[str(-1*i), 'Count']
            iter+=1

        iter=0
        for i in range(1,5):
            

            data_frame.at[iter, 'Octant ID new'] = str(i)
            data_frame.at[iter, 'Longest Subsequence Length new'] = temp_df.at[str(i), 'Len']
            
            data_frame.at[iter, 'Count new'] = temp_df.at[str(i), 'Count']
            iter+=1
            data_frame.at[iter, 'Octant ID new'] = "Time"
            data_frame.at[iter, 'Longest Subsequence Length new'] = "From"
            
            data_frame.at[iter, 'Count new'] = "To"
            iter+=1
            for index in range(0, len(temp_df_1[str(i)]), 2):
                if np.isnan(temp_df_1.at[index, str(i)]):
                    break
                data_frame.at[iter, 'Longest Subsequence Length new'] = temp_df_1.at[index, str(i)]
                data_frame.at[iter, 'Count new'] = temp_df_1.at[index+1, str(i)]
                iter+=1

            data_frame.at[iter, 'Octant ID new'] = str(-1*i)
            data_frame.at[iter, 'Longest Subsequence Length new'] = temp_df.at[str(-1*i), 'Len']
            
            data_frame.at[iter, 'Count new'] = temp_df.at[str(-1*i), 'Count']
            iter+=1
            data_frame.at[iter, 'Octant ID new'] = "Time"
            data_frame.at[iter, 'Longest Subsequence Length new'] = "From"
            
            data_frame.at[iter, 'Count new'] = "To"
            iter+=1
            
            for index in range(0, len(temp_df_1[str(-1*i)]), 2):
                if np.isnan(temp_df_1.at[index, str(-1*i)]):
                    break
                data_frame.at[iter, 'Longest Subsequence Length new'] = temp_df_1.at[index, str(-1*i)]
                data_frame.at[iter, 'Count new'] = temp_df_1.at[index+1, str(-1*i)]
                iter+=1     

    except Exception as e:
        print(e)
        exit()

    
    writing_excel_file("output_octant_longest_subsequence_with_range.xlsx")


if __name__ == "__main__":
    ver = python_version()

    if ver == "3.8.10":
        print("Correct Version Installed")
    else:
        print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")

    mod = 10000
    octact_identification(mod)