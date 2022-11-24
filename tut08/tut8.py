import pandas as pd
from datetime import datetime
from platform import python_version
ver = python_version()
start_time = datetime.now()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def file_read(file1, file2, file3):
    try:
        file_1 = open(file1,'r')
        Lines_1 = file_1.readlines()
        file_2 = open(file2, 'r')
        Lines_2 = file_2.readlines()
        file_3 = open(file3,'r')
        Lines_3 = file_3.readlines()
        runs = {}
        runs['no run'] = 0
        runs['1 run'] = 1
        runs['2 runs'] = 2
        runs['3 runs'] = 3
        runs['FOUR'] = 4
        runs['SIX'] = 6
    except:
        print("Error in reading the files")
        exit()
    return runs, Lines_1, Lines_2, Lines_3

def Full_nm(nm,lst):
    for i in range(len(lst)):
        if nm in lst[i]:
            break
    return lst[i]

def nm(nm):
    nm = nm.split(" ")
    nm = nm[1:len(nm)+1]
    nm = " ".join(nm)
    return nm

def Over(over):
    over = over.split(" ")
    over = over[0]
    return over

def over_num(x):
    over = ""
    if x%6==0:
        over = str(x/6)
    else:
        over = str(x//6) + "." +str(x%6)
    return over

def group_div(group_nm,lst):
    for i in range(2):
        if group_nm in lst[i].split(":")[0]:
            break
    x = lst[i].split(": ")
    players  = x[1]
    players = players.split(", ")
    last_player = ""
    for i in players[-1]:
        if i != "\n":
            last_player+=i
    players[-1] = last_player
    return players

def commentary_lines(Lines):
    lines = []
    for i in range(len(Lines)):
        if Lines[i] !="\n":
            lines.append(Lines[i])
    return lines
