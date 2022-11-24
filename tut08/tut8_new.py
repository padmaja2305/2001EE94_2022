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

def Full_name(name,List):
    for i in range(len(List)):
        if name in List[i]:
            break
    return List[i]

def Name(name):
    name = name.split(" ")
    name = name[1:len(name)+1]
    name = " ".join(name)
    return name

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

def Team_Division(Team_name,List):
    for i in range(2):
        if Team_name in List[i].split(":")[0]:
            break
    x = List[i].split(": ")
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
def Team_data(lines,Batting_team,Bowling_team):
    Data = []
    for line in lines:
        Dict = {}
        Dict_1 = {}
        line = line.split(', ')
        Dict["Batsman"] = Full_name(line[0].split('to ')[1], Batting_team)
        Dict["Bowler"] = Full_name(Name(line[0].split(' to')[0]),Bowling_team)
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


def Bat_Bowl_order(List):
    list_1 = []
    List2 = []
    List1 = []
    for i in List:
        if i["Batsman"] not in List1:
            List1.append(i["Batsman"])
        if i["Bowler"] not in List2:
            List2.append(i["Bowler"])
    list_1.append(List1)
    list_1.append(List2)
    return list_1
#-----------------------Getting the bowling dataset for both the teams-------------------------
def Bowling_Data_Set(index,List,List1, runs):
    data = []
    data_set = pd.DataFrame(data,index = index, columns = [])
    data_set.insert(0,column = "b",value="")
    data_set.insert(1,column = "m",value="0")
    data_set.insert(2,column = "r",value= 0)
    data_set.insert(3,column = "w",value = 0)
    data_set.insert(4,column = "nb",value = "0")
    data_set.insert(5,column = "wd",value = 0)
    data_set.insert(6,column = "Eco", value=0)
    for i in List:
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

    for i in List1:
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
    final = {"Bowler":List1,"b":b,"o":m,"r":r,"w":w,"nb":nb,"wd":wd,"ECO":ECO}
    Final = pd.DataFrame(final)

    return Final
#---------------------------------Getting the batting dataset for both the teams------------------------
def Batting_Data_Set(index,List,List2, runs):
    outs = 0
    data =[]
    data_set = pd.DataFrame(data,index = index, columns = [])
    cols = ["Stats","Runs","Balls","4s","6s","SR"]
    for i in range(len(cols)):
        data_set.insert(i,column = cols[i],value = "")
    for i in List:
        if "wide"not in i["Run"] and "out" not in i["Run"]:
            data_set.at[i["Batsman"],"Stats"] += i["Run"] +","
        if "out" in i["Run"]:
            outs+=1
            data_set.at[i["Batsman"],"Stats"] += i["Run"] + " b "+ i["Bowler"] +","
    for i in List2:
        stats = data_set.at[i,"Stats"].split(",")
        stats.remove(stats[-1])
        data_set.at[i,"Stats"] = stats
    wides = 0
    leg_byes = 0
    byes = 0
    no_ball = 0
    for i in List:
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

    for i in List2:
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
    New = "{} ({} wkts, {} Ov)".format(tot,outs,List[-1]["Over"])
    List2.extend(["Extras","Total"])
    tot_runs.extend([new,New])
    out_not_out.extend(["",""])
    tot_balls.extend(["",""])
    tot_fours.extend(["",""])
    tot_six.extend(["",""])
    SR.extend(["",""])
    ret_data = {"Batter" : List2, "":out_not_out,"R":tot_runs,"B":tot_balls,"4s":tot_fours,"6s":tot_six,"SR":SR}
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
#----------------To get fallofwickets of each team ----------------------------------------------
def Fallofwickets(List, runs):
    Runs = 0
    List_1 = []
    wic = 0
    for i in List:
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
            List_1.append(Str)
    return List_1
#-----------------------List of players who did not bat from each team-----------------
def Did_not_bat(List1,List2):
    list3 = []
    for i in List1:
        if i not in List2:
            list3.append(i)
    return list3
#------------------------Runs scored in powerplay---------------------------------------
def powerplay(List1):
    power = 0
    for i in List1:
        if i["Over"] == "6.1":
            break
        else:
            power+=runs_counter(i["Run"])
    return power
#----------------------Team scorecard for each teams ------------------------------------
def Team_scorecard(index,Batting_Frame1,Bowling_Frame2,Did_not,Fall,powerRun):
    scorecard = pd.DataFrame()
    for i in range(8):
        scorecard.insert(i, column = str(i),value="")
    shape_0 = scorecard.shape
    shape_1 = Batting_Frame1.shape
    shape_3 = Bowling_Frame2.shape
    c = 0
    for i in Batting_Frame1.columns:
        scorecard.at[index,str(c)] = i
        c+=1
    index+=1
    for i in range(shape_1[0]):
        for j in range(shape_1[1]):
            scorecard.at[index,str(j)] = Batting_Frame1.iloc[i,j]
        index+=1
    if len(Did_not)!=0: 
        scorecard.at[index,"0"] = "Did not Bat"
        for i in range(len(Did_not)):
            scorecard.at[index,str(i+1)] = Did_not[i]
        index+=1
    for i in range(8):
        scorecard.at[index,str(i)] = " "
    index+=1
    scorecard.at[index,"0"] = "Fall Of Wickets"
    index+=1
    count = 0
    col = 0
    pak_wic = Fall
    while count!=len(pak_wic):
        if col == shape_0[1]:
            index +=1
            col = 0
        scorecard.at[index,str(col)] = pak_wic[count]
        col+=1
        count+=1
    index+=1
    for i in range(8):
        scorecard.at[index,str(i)] = " "
    index+=1
    new_cols = ["Bowler","O","M","R","W","NB","WD","ECO"]
    for i in range(len(new_cols)):
        scorecard.at[index,str(i)] = new_cols[i]
    index+=1
    for i in range(shape_3[0]):
        for j in range(shape_3[1]):
            scorecard.at[index,str(j)] = Bowling_Frame2.iloc[i,j]
        index+=1
    for i in range(8):
        scorecard.at[index,str(i)] = " "
    index+=1
    scorecard.at[index,"0"] = "Powerplays"
    scorecard.at[index,"2"] = "Overs"
    scorecard.at[index,"7"] = "Runs"
    index+=1
    scorecard.at[index,"0"] = "Mandatory"
    scorecard.at[index,"2"] = "0.1-6"
    scorecard.at[index,"7"] = powerRun
    index+=1
    for i in range(8):
        scorecard.at[index,str(i)] = " "
    index+=1
    return scorecard,index

def main(file1, file2, file3):
    runs, Lines_1, Lines_2, Lines_3 = file_read(file1, file2, file3)

    try:
        #Obtaining lines from the text file
        lines_1,lines_2,lines_3 = commentary_lines(Lines_1),commentary_lines(Lines_2),commentary_lines(Lines_3)

        #Obtaining Players of both the teams
        Indian_players = Team_Division("India",lines_1)
        Pakistan_players = Team_Division("Pakistan",lines_1)

        #Generating Raw Data for both the teams
        India_Data, Pakistan_Data = Team_data(lines_2,Indian_players,Pakistan_players), Team_data(lines_3,Pakistan_players,Indian_players)

        #Batting/Bowling order of both the teams   
        Pakistan_Batting = Bat_Bowl_order(Pakistan_Data)
        India_Batting = Bat_Bowl_order(India_Data)

        #Batting dataset for each team
        India_Batting_set = Batting_Data_Set(India_Batting[0],India_Data,India_Batting[0], runs)
        Pakistan_Batting_set = Batting_Data_Set(Pakistan_Batting[0],Pakistan_Data,Pakistan_Batting[0], runs)

        #Bowling set for each team
        India_Bowling_set = Bowling_Data_Set(Pakistan_Batting[1],Pakistan_Data,Pakistan_Batting[1], runs)
        Pakistan_Bowling_set = Bowling_Data_Set(India_Batting[1],India_Data,India_Batting[1], runs)

        #Players who did not bat from each team
        Pakistan_did_not_bat = Did_not_bat(Pakistan_players,Pakistan_Batting[0])
        India_did_not_bat = Did_not_bat(Indian_players,India_Batting[0])

        #Fall of wickets of each team
        India_fall_of_wickets = Fallofwickets(India_Data, runs)
        Pakistan_fall_of_wickets = Fallofwickets(Pakistan_Data, runs)

        # Powerplay run scored by each team 
        India_Power_play = powerplay(India_Data)
        Pakistan_Power_play = powerplay(Pakistan_Data)

        # Team scorecard of each team
        Pakistan_score,Index1 = Team_scorecard(0,Pakistan_Batting_set,India_Bowling_set,Pakistan_did_not_bat,Pakistan_fall_of_wickets,Pakistan_Power_play)
        India_score,Index2 = Team_scorecard(Index1+1,India_Batting_set,Pakistan_Bowling_set,India_did_not_bat,India_fall_of_wickets,India_Power_play)
    except:
        print("Error")
        exit()

    try:
    #--------------------------------- Concatenating scorecard dataframes of each team into final scorecard-------------------------
        Frames = [Pakistan_score,India_score]
        Scorecard = pd.concat(Frames)
    except:
        print("Error in concatenating two dataframes")
        exit()
    try:
    #----------------------------------- Final scorecard csv file -------------------------------- 
        Scorecard.to_csv("Scorecard.csv",index = False, header = False)
    except:
        print("Error in giving the output file")
        exit()

if __name__ == "__main__":
    if ver == "3.8.10":
        print("Correct Version Installed")
    else:
        print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")
    main('teams.txt', 'india_inns.txt', 'pak_inns1.txt')

    end_time = datetime.now()
    print('Duration of Program Execution: {}'.format(end_time - start_time))