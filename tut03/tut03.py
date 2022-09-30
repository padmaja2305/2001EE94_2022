from glob import glob
from platform import python_version
import pandas as pd
import numpy as np
import math

data_frame = None
rows = None
idx = 0

def reading_excel_file(filename):
    global data_frame
    global rows
    try:
        data_frame = pd.read_excel("input_octant_transition_identify.xlsx")
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
    global idx
    try:
        # Split list into ranges and find the count of octant values
        start = 0
        end = len(l)
        step = int(mod)
        idx = 2
        total_rows_mod = math.ceil(rows/step)
        for i in range(start, end, step):
            x = i
            sub_list = l[x:x+step]
            y = x+step-1
            if y > rows:
                y = rows-1
            data_frame.at[idx, 'Octant ID'] = str(x)+"-"+str(y)
            data_frame.at[idx, '1'] = sub_list.count(1)
            data_frame.at[idx, '-1'] = sub_list.count(-1)
            data_frame.at[idx, '2'] = sub_list.count(2)
            data_frame.at[idx, '-2'] = sub_list.count(-2)
            data_frame.at[idx, '3'] = sub_list.count(3)
            data_frame.at[idx, '-3'] = sub_list.count(-3)
            data_frame.at[idx, '4'] = sub_list.count(4)
            data_frame.at[idx, '-4'] = sub_list.count(-4)
            idx += 1

        # Verified Column
        data_frame.at[idx, 'Octant ID'] = "Verified"
        for i in range(-4, 5):
            if i == 0:
                continue
            data_frame.at[idx, str(i)] = data_frame[str(
                i)].iloc[2:(2+total_rows_mod)].sum()
    except:
        print("Error in counting octant values for ranges.")
        exit()

def transistion_count():
    global data_frame
    global idx
    try:
        # -------------- Overall Transition Count ----------------------

        idx += 3
        data_frame.at[idx, 'Octant ID'] = "Overall Transition Count"
        idx += 1
        data_frame.at[idx, '1'] = 'To'
        idx += 1
        data_frame.at[idx, 'Octant ID'] = 'Count'
        for k in range(-4, 5):
            if k == 0:
                continue
            data_frame.at[idx, str(k)] = k
        idx += 1
        data_frame.at[idx, ''] = "From"

        # Creating dataframe to store values
        data = []
        data_frame2 = pd.DataFrame(data, index=['1', '-1', '2', '-2', '3', '-3', '4', '-4'],
                                   columns=['1', '-1', '2', '-2', '3', '-3', '4', '-4'])

        data_frame2 = data_frame2.fillna(0)

        # Calculating values
        for i in range(0, rows-1):
            first = str(data_frame.at[i, 'Octant'])
            second = str(data_frame.at[i+1, 'Octant'])
            data_frame2.at[first, second] += 1

        # Adding values to main dataframe
        for k in range(1, 5):
            data_frame.at[idx, 'Octant ID'] = str(k)
            for l in range(-4, 5):
                if l == 0:
                    continue
                data_frame.at[idx, str(l)] = data_frame2.at[str(k), str(l)]
            idx += 1
            data_frame.at[idx, 'Octant ID'] = str(-1*k)
            for l in range(-4, 5):
                if l == 0:
                    continue
                data_frame.at[idx, str(l)] = data_frame2.at[str(-1*k), str(l)]
            idx += 1
    except:
        print("Error in calculating Overall Transition Count.")
        exit()

def mod_transiston(mod):
    global data_frame
    global idx
    step = int(mod)
    try:
        # ------------ Mod Transition Count ------------------
        for i in range(0, rows, step-1):
            lim = i+step-1
            if lim >= rows:
                lim = rows-1
            idx += 2
            data_frame.at[idx, 'Octant ID'] = 'Mod Transition Count'
            idx += 1
            data_frame.at[idx, 'Octant ID'] = str(i)+'-'+str(lim)
            data_frame.at[idx, '1'] = 'To'
            idx += 1
            data_frame.at[idx, 'Octant ID'] = 'Count'
            for k in range(-4, 5):
                if k == 0:
                    continue
                data_frame.at[idx, str(k)] = k
            idx += 1
            data_frame.at[idx, ''] = "From"

            # Creating dataframe to store values
            data = []
            data_frame2 = pd.DataFrame(data, index=['1', '-1', '2', '-2', '3', '-3', '4', '-4'],
                                       columns=['1', '-1', '2', '-2', '3', '-3', '4', '-4'])
            data_frame2 = data_frame2.fillna(0)

            # Calculating values
            for j in range(i, lim):
                first = str(data_frame.at[j, 'Octant'])
                second = str(data_frame.at[j+1, 'Octant'])
                data_frame2.at[first, second] += 1

            # Adding values to main dataframe
            for k in range(1, 5):
                data_frame.at[idx, 'Octant ID'] = str(k)
                for l in range(-4, 5):
                    if l == 0:
                        continue
                    data_frame.at[idx, str(l)] = data_frame2.at[str(k), str(l)]
                idx += 1
                data_frame.at[idx, 'Octant ID'] = str(-1*k)
                for l in range(-4, 5):
                    if l == 0:
                        continue
                    data_frame.at[idx, str(
                        l)] = data_frame2.at[str(-1*k), str(l)]
                idx += 1
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



def octact_identification(mod):
    global data_frame
    reading_excel_file("input_octant_transition_identify.xlsx")
    average()
    insert_octant_column()
    l = insert_octant_values()
    # count_ocatant_value(l)
    # transistion_count()
    # mod_transiston(mod)
    try:
        data = []
        column_data = data_frame['Octant'].tolist()
        prev = -1
        for i in [-4,-3,-2,-1,1,2,3,4]:
            subsequence = 0
            longest_subsequence = 0
            count = 0
            for j in column_data:
                if j == i:
                    subsequence += 1
                    if subsequence == longest_subsequence:
                        count += 1
                    elif subsequence > longest_subsequence:
                        longest_subsequence = subsequence
                        count = 1
                else:
                    subsequence = 0
                prev = j
            data.append([i, longest_subsequence, count])
        print(data, subsequence, longest_subsequence, count)
        data_frame.insert(13, "Octant_ID", "")
        data_frame.insert(14, "Longest Subsequence", "")
        data_frame.insert(15, "Count", "")
        n = 0
        for i in data:
            data_frame.at[n, 'Octant_ID'] = i[0]
            data_frame.at[n, 'Longest Subsequence'] = i[1]
            data_frame.at[n, 'Count'] = i[2]
            n += 1
    except Exception as e:
        print(e)
        exit()

    
    writing_excel_file("output_octant_transition_identity.xlsx")


if __name__ == "__main__":
    ver = python_version()

    if ver == "3.8.10":
        print("Correct Version Installed")
    else:
        print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")

    mod = 10000
    octact_identification(mod)