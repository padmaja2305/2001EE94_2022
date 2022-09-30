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


        
#This shall be the last lines of the code.
end_time = datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))
