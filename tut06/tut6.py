# imports

import pandas as pd
import numpy as np
from datetime import timedelta
from datetime import date
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

import csv
from random import randint
from time import sleep
from datetime import datetime
from platform import python_version

ver = python_version()
timestamp = datetime.now()

def read_file(stud_file, att_file):
    try:
        df_reg = pd.read_csv(stud_file)
        df_attendance = pd.read_csv(att_file)
    except Exception as e:
        print("Error in reading CSV Files.", e)
    return df_reg, df_attendance

def read_student_file(df_reg):
    try:
        ttl_stud = df_reg.shape[0]
        roll_nm={}
        lst_roll = []
        for idx in range(ttl_stud):
            roll_nm[df_reg.at[idx, "Roll No"]] = df_reg.at[idx, "Name"]
            lst_roll.append(df_reg.at[idx, "Roll No"])
    except Exception as e:
        print("Error in reading Input Registered Students.", e)
    return  roll_nm

def store_dates(df_attendance):
    try:   
        #-------------------LIST TO STORE VALID DATES-------------------------
        net_attendance = df_attendance.shape[0]
        net_dates = set()
        for timestamp in df_attendance["Timestamp"]:
            date = timestamp.split(" ")[0]
            net_dates.add(date)
        
        # sorting dates
        net_dates = list(net_dates)
        net_dates.sort(key=lambda date: datetime.strptime(date, "%d-%m-%Y"))
        
        # removing invalid date from top and bottom
        for date in net_dates:
            date_split = date.split("-")
            day = pd.to_datetime(datetime(int(date_split[2]), int(date_split[1]), int(date_split[0]))).weekday()
            if(day==0 or day==3):
                break
            net_dates.remove(date)
        
        for idx in range(len(net_dates)-1, 0, -1):
            date = net_dates[idx]
            date_split = date.split("-")
            day = pd.to_datetime(datetime(int(date_split[2]), int(date_split[1]), int(date_split[0]))).weekday()
            if(day==0 or day==3):
                break
            net_dates.remove(date)
        
        date_split = net_dates[0].split("-")
        start_date = pd.to_datetime(datetime(int(date_split[2]), int(date_split[1]), int(date_split[0])))
        
        date_split = net_dates[-1].split("-")
        end_date = pd.to_datetime(datetime(int(date_split[2]), int(date_split[1]), int(date_split[0])))
        
        # req_dates -> store all valid Mondays and Thursdays
        req_dates = []
        date_idx = {}
        idx=1
        while start_date <= end_date:
            date_str = start_date.date().strftime("%d-%m-%Y")
            req_dates.append(date_str) 
            date_idx[date_str] = idx
            idx+=1
            day = start_date.weekday()
            if day==0:
                start_date = start_date + timedelta(days=3)
            elif day==3:
                start_date = start_date + timedelta(days=4)
    except Exception as e:
        print("Error in creating a list of valid dates.", e)
    return req_dates, date_idx

def create_dataframe(roll_nm, df_attendance, date_idx, req_dates):
    try:
        #---------------CREATRING DATAFRAMES TO STORE OUTPUT--------------
        
        # df_con -> attendance_report_consolidated
        # TO STORE CONSOLIDATED REPORT
        data_ini = []
        df_con = pd.DataFrame(data_ini, columns=["Roll","Name"]+req_dates+["Actual Lecture Taken", "net Real", "% Attendance"])
        con_row = 0
        for roll, name in roll_nm.items():
            # creating a dataframe to store individual report
            df_indi = pd.DataFrame(data_ini, columns=['Date',
                                                    'Roll',
                                                    'Name',
                                                    'net Attendance Count',
                                                    'Real',
                                                    'Duplicate',
                                                    'Invalid',
                                                    'Absent'])
            df_indi.at[0,'Name'] = name
            df_indi.at[0,'Roll'] = roll
            df_con.at[con_row, 'Roll'] = roll
            df_con.at[con_row, 'Name'] = name
            df_con.at[con_row, 'Actual Lecture Taken'] = len(req_dates)
            
            # default values to all cells
            for idx, date in enumerate(req_dates, start=1):
                df_indi.at[idx, 'Date'] = date
                df_indi.at[idx, 'net Attendance Count'] = 0
                df_indi.at[idx, 'Real'] = 0
                df_indi.at[idx, 'Duplicate'] = 0
                df_indi.at[idx, 'Invalid'] = 0
                df_indi.at[idx, 'Absent'] = 1
                df_con.at[con_row, date] = 'A'
            
            # calculating required values and storing them in dataframe
            for timestamp, details in zip(df_attendance['Timestamp'], df_attendance['Attendance']):
                roll_no = details[0:8]
                if(roll_no != roll):
                    continue
                date = timestamp.split(" ")[0]
                time = timestamp.split(" ")[1]
                if date not in req_dates:
                    continue
                index = date_idx[date]
                df_indi.at[index, 'net Attendance Count'] += 1
                time_split = time.split(":")
                if (time_split[0]=='14') or (time=="15:00"):
                    if df_indi.at[index, 'Real'] == 0:
                        df_indi.at[index, 'Real'] = 1
                    else:
                        df_indi.at[index, 'Duplicate'] += 1
                else:
                    df_indi.at[index, 'Invalid'] += 1
                
                if df_indi.at[index, 'Real'] == 1 :
                    df_indi.at[index, 'Absent'] = 0
                    df_con.at[con_row, date] = 'P'
            
            # To find net Real
            df_con.at[con_row, 'net Real']=0
            for date in req_dates:
                if df_con.at[con_row, date]=='P':
                    df_con.at[con_row, 'net Real']+=1
            
            df_con.at[con_row, '% Attendance'] = round(df_con.at[con_row, 'net Real']*100 / len(req_dates), 2)
            
            # increment in rows for df_con
            con_row+=1
                    
            # generating individual excel reports
            df_indi.to_excel(f"output/{roll}.xlsx", index=False)
    except Exception as e:
        print("Error in generating individual attendance reports.", e)
    

    try:
        # generating consolidated attendance report
        df_con.to_excel("output/attendance_report_consolidated.xlsx", index=False)
    except Exception as e:
        print("Error in generating COnsolidated Attendance report.", e)

