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
