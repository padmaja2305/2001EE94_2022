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
#------- Reading and converting the data from text file to dictionary --------------
def group_data(lines,Batting_group,Bowling_group):
    Data = []
    for line in lines:
        Dict = {}
        Dict_1 = {}
        line = line.split(', ')
        Dict["Batsman"] = Full_nm(line[0].split('to ')[1], Batting_group)
        Dict["Bowler"] = Full_nm(nm(line[0].split(' to')[0]),Bowling_group)
        Dict["Over"] = Over(line[0].split(' to')[0])
        if "leg byes" in line[1] or "no ball" in line[1] or "byes" in line[1]:
            Dict["Run"] = line[1] + "-" + line[2]
        else:
            if "out" in line[1]:
                x = line[1].split("!!")[0]
                if "Caught" in x:
                    y = x.split("Caught by")
                    Dict["Run"] = y[0] +"c" + y[1]
                else:
                    Dict["Run"] = x
            else:
                Dict["Run"] = line[1]
        Data.append(Dict)
    return Data


def Bat_Bowl_order(lst):
    lst_1 = []
    lst2 = []
    lst1 = []
    for i in lst:
        if i["Batsman"] not in lst1:
            lst1.append(i["Batsman"])
        if i["Bowler"] not in lst2:
            lst2.append(i["Bowler"])
    lst_1.append(lst1)
    lst_1.append(lst2)
    return lst_1
#-----------------------Getting the bowling dataset for both the groups-------------------------
def Bowling_Data_Set(index,lst,lst1, runs):
    data = []
    data_set = pd.DataFrame(data,index = index, columns = [])
    data_set.insert(0,column = "b",value="")
    data_set.insert(1,column = "m",value="0")
    data_set.insert(2,column = "r",value= 0)
    data_set.insert(3,column = "w",value = 0)
    data_set.insert(4,column = "nb",value = "0")
    data_set.insert(5,column = "wd",value = 0)
    data_set.insert(6,column = "Eco", value=0)
    for i in lst:
        data_set.at[i["Bowler"],"b"] += str(i["Over"]) + ","
        if "out" not in i["Run"]:
            if i["Run"] in runs.keys():
                data_set.at[i["Bowler"],"r"] +=runs[i["Run"]]
            elif "wides" in i["Run"]:
                data_set.at[i["Bowler"],"wd"] += int(i["Run"].split(" ")[0])
                data_set.at[i["Bowler"],"r"]  += int(i["Run"].split(" ")[0])

            elif i["Run"]=="wide":
                data_set.at[i["Bowler"],"wd"] += 1
                data_set.at[i["Bowler"],"r"]  += 1

        else:
            val3 = data_set.at[i["Bowler"],"w"]
            val3+=1
            data_set.at[i["Bowler"],"w"] = val3

    for i in lst1:
        var1 = data_set.at[i,"b"].split(",")
        var1.remove(var1[-1])
        var2 = set(var1)
        data_set.at[i,"b"] = over_num(len(var2))
        data_set.at[i,"Eco"] = round(data_set.at[i,"r"]*6/len(var2),2)
    b = [i for i in data_set["b"]]
    m = [i for i in data_set["m"]]
    nb =[i for i in data_set["nb"]]
    r = [i for i in data_set["r"]]
    w = [i for i in data_set["w"]]
    wd =[i for i in data_set["wd"]]
    ECO = [i for i in data_set["Eco"]]
    final = {"Bowler":lst1,"b":b,"o":m,"r":r,"w":w,"nb":nb,"wd":wd,"ECO":ECO}
    Final = pd.DataFrame(final)

    return Final
#---------------------------------Getting the batting dataset for both the groups------------------------
def Batting_Data_Set(index,lst,lst2, runs):
    outs = 0
    data =[]
    data_set = pd.DataFrame(data,index = index, columns = [])
    cols = ["Stats","Runs","Balls","4s","6s","SR"]
    for i in range(len(cols)):
        data_set.insert(i,column = cols[i],value = "")
    for i in lst:
        if "wide"not in i["Run"] and "out" not in i["Run"]:
            data_set.at[i["Batsman"],"Stats"] += i["Run"] +","
        if "out" in i["Run"]:
            outs+=1
            data_set.at[i["Batsman"],"Stats"] += i["Run"] + " b "+ i["Bowler"] +","
    for i in lst2:
        stats = data_set.at[i,"Stats"].split(",")
        stats.remove(stats[-1])
        data_set.at[i,"Stats"] = stats
    wides = 0
    leg_byes = 0
    byes = 0
    no_ball = 0
    for i in lst:
        if "wides" in i["Run"]:
            wides += int(i["Run"].split(" ")[0])
        if i["Run"] == "wide":
            wides+=1
        if "leg" in i["Run"] and "byes" in i["Run"]:
            leg_byes += runs[i["Run"].split("-")[1]]
        if "byes" in i["Run"] and "leg" not in i["Run"]:
            byes+= runs[i["Run"].split("-")[1]]
        if "no ball" in i["Run"]:
            no_ball += runs[i["Run"].split("-")[1]]

    for i in lst2:
        score = 0
        six = 0
        four = 0
        balls = 0
        for j in data_set.at[i,"Stats"]:
            if "wide" not in j:
                balls+=1
                data_set.at[i,"Balls"] = balls

            if j in runs.keys():
                score += runs[j]
                data_set.at[i,"Runs"] = score
                if j=="FOUR":
                    four +=1
                    data_set.at[i,"4s"] = four
                if j=="SIX":
                    six +=1
                    data_set.at[i,"6s"] = six
        if data_set.at[i,"Runs"] =="":
            data_set.at[i,"Runs"] = 0
        if data_set.at[i,"4s"] =="":
            data_set.at[i,"4s"] = 0
        if data_set.at[i,"6s"] =="":
            data_set.at[i,"6s"] = 0
        data_set.at[i,"SR"] = round(score*100/balls,2)
        if "out" in j:
            data_set.at[i,"Stats"] = j.split("out")[1]
        else:
            data_set.at[i,"Stats"] = "not out"
    out_not_out = [i for i in data_set["Stats"]]
    tot_runs = [i for i in data_set["Runs"]]
    tot_balls = [i for i in data_set["Balls"]]
    tot_fours = [i for i in data_set["4s"]]
    tot_six = [i for i in data_set["6s"]]
    SR = [i for i in data_set["SR"]]
    extras =  wides+leg_byes+byes+no_ball
    new = "{} (b {}, lb {}, w{}, nb {})".format(extras,byes,leg_byes,wides,no_ball)
    tot = data_set["Runs"].sum() + extras
    New = "{} ({} wkts, {} Ov)".format(tot,outs,lst[-1]["Over"])
    lst2.extend(["Extras","Total"])
    tot_runs.extend([new,New])
    out_not_out.extend(["",""])
    tot_balls.extend(["",""])
    tot_fours.extend(["",""])
    tot_six.extend(["",""])
    SR.extend(["",""])
    ret_data = {"Batter" : lst2, "":out_not_out,"R":tot_runs,"B":tot_balls,"4s":tot_fours,"6s":tot_six,"SR":SR}
    Data_Set = pd.DataFrame(ret_data)
    return Data_Set

def runs_counter(run, runs):
    Runs = 0
    if "out" not in run:
        if run in runs.keys():
            Runs+= runs[run]
        elif "byes" in run or "no ball" in run:
                Runs+=runs[run.split("-")[1]]
        elif "wides" in run:
            Runs +=int(run.split(" ")[0])
        elif run=="wide":
            Runs+=1
    return Runs
#----------------To get fallofwickets of each group ----------------------------------------------
def Fallofwickets(lst, runs):
    Runs = 0
    lst_1 = []
    wic = 0
    for i in lst:
        if "out" not in i["Run"]:
            if i["Run"] in runs.keys():
                Runs +=runs[i["Run"]]
            elif "byes" in i["Run"] or "no ball" in i["Run"]:
                Runs+=runs[i["Run"].split("-")[1]]
            elif "wides" in i["Run"]:
                Runs +=int(i["Run"].split(" ")[0])
            elif i["Run"]=="wide":
                Runs+=1
        else:
            wic+=1
            Str = str(Runs) + "-" + str(wic) + "( " + i["Batsman"] + ", " + i["Over"] +")" 
            lst_1.append(Str)
    return lst_1
