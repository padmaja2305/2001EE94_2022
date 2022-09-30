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
        data = []
        column_data = df.at['Octant']

        prev = -1
        for i in [-4,-3,-2,-1,1,2,3,4]:
            subsequence = 0
            longest_subsequence = 0
            count = 0
            for j in column_data:
                if j == i:
                    subsequence += 1
                else:
                    subsequence = 0
                    if subsequence == longest_subsequence:
                        count += 1
                    elif subsequence > longest_subsequence:
                        longest_subsequence = subsequence
                        count = 1
                    prev = i
            data.append([i, longest_subsequence, count])

        for i in data:
            df.at[i[0], 'Octant ID'] = i[0]
            df.at[i[0], 'Longest Subsequence Length'] = i[1]
            df.at[i[0], 'Count'] = i[2]
    except Exception as e:
        print(e)
        exit()

#This shall be the last lines of the code.
end_time = datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))
