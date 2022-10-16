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

