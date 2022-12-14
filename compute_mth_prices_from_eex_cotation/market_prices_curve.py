# -*- coding: utf-8 -*-
"""
Created on Sun Sep  4 17:14:42 2022

@author: hermann.ngayap
"""

import os
from datetime import datetime 
import time
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
from datetime import timedelta
import numpy as np
from datetime import datetime as dt
pd.options.display.float_format = '{:.3f}'.format
path=r'C:/Users/hermann.ngayap/Boralex/Marchés Energie - FR - Equipe Marchés - Gestion de portefeuille/in/'

print("The working directory was: {0}".format(os.getcwd()))
os.chdir("C:/Users/hermann.ngayap/Boralex/Marchés Energie - FR - Equipe Marchés - Gestion de portefeuille/in")
print("The current working directory is: {0}".format(os.getcwd()))

#Open SQL connection to fetch monthly prices data derrived from price curve
import pyodbc
import sqlalchemy
from sqlalchemy import create_engine, event
from server_credentials import server_credentials

mths_remaining=12-dt.today().month
nb_months=12
nb_quarters=24
nb_eex_qb_cotation=5
nb_years=(2028-dt.today().year)#change the year to the year that suits the most your horizon
horizon_m=nb_months*nb_years-2#remove the month of July/Aug. we are now in Sep
horizon_q=nb_quarters-nb_eex_qb_cotation

mb=pd.read_excel(path+'Futures_products_2022.xlsx', sheet_name='MB')
mb=mb.iloc[0:6,:]
qb=pd.read_excel(path+'Futures_products_2022.xlsx', sheet_name='QB')
qb=qb.iloc[0:6,:]
yb=pd.read_excel(path+'Futures_products_2022.xlsx', sheet_name='YB')
yb=yb.iloc[0:6,:]

q_weights=pd.read_excel(path+'q_weights.xlsx', sheet_name='Qw')
m_weights=pd.read_excel(path+'m_weights.xlsx', sheet_name='Mw')

#=================================Years=================================

yb['years']=["20"+yb['Delivery Period'][i][-2:] for i in range(len(yb))]
yb['years']=pd.to_numeric(yb['years'])

#=================================Quarters==============================

qb['Period']=["20"+qb['Delivery Period'][i][-2:]+"-0"+ qb['Delivery Period'][i][0]+"-01" for i in range(len(qb))]
qb['years']=[qb['Period'][i][:4] for i in range(len(qb))]
qb['years']=qb['years'].astype(int)
qb['quarters']=[qb['Period'][i][6] for i in range(len(qb))]
qb['quarters']=qb['quarters'].astype(int)
qb['Period']=pd.to_datetime(qb['Period'])

qb_=qb.iloc[6:,:]
list_q=[]
date_start=qb['Period'][5]
for i in range(horizon_q): 
    date_start += pd.DateOffset(months=3)
    list_q.append(date_start)

#Extrapolation quarterly prices
qb_temp = pd.DataFrame({'Period': list_q})
qb_temp['Date']='NaN'
qb_temp['Delivery Period']='NaN'
qb_temp['Settlement Price'] = "NaN" 
qb_temp=qb_temp[['Date', 'Delivery Period', 'Settlement Price', 'Period']]
qb_temp['years']=qb_temp['Period'].dt.year
qb_temp['quarters']=qb_temp['Period'].dt.quarter
   
price=[]
for idx, row in qb_temp.iterrows():
    year=row['years']
    quarter=row['quarters']
    if (year==2024) & (quarter==2):
        price.append( yb.loc[yb['years']==2024, 'Settlement Price'] * float(q_weights.loc[q_weights['quarters']==2, 'weights']))        
    elif (year==2024) & (quarter==3):
        price.append( yb.loc[yb['years']==2024, 'Settlement Price'] * float(q_weights.loc[q_weights['quarters']==3, 'weights']))
    elif (year==2024) & (quarter==4):
        price.append( yb.loc[yb['years']==2024, 'Settlement Price'] * float(q_weights.loc[q_weights['quarters']==4, 'weights']))
    elif (year==2025) & (quarter==1):
        price.append( yb.loc[yb['years']==2025, 'Settlement Price'] * float(q_weights.loc[q_weights['quarters']==1, 'weights']))
    elif (year==2025) & (quarter==2):
        price.append( yb.loc[yb['years']==2025, 'Settlement Price'] * float(q_weights.loc[q_weights['quarters']==2, 'weights']))
    elif (year==2025) & (quarter==3):
        price.append( yb.loc[yb['years']==2025, 'Settlement Price'] * float(q_weights.loc[q_weights['quarters']==3, 'weights']))
    elif (year==2025) & (quarter==4):
        price.append( yb.loc[yb['years']==2025, 'Settlement Price'] * float(q_weights.loc[q_weights['quarters']==4, 'weights']))
    elif (year==2026) & (quarter==1):
        price.append( yb.loc[yb['years']==2026, 'Settlement Price'] * float(q_weights.loc[q_weights['quarters']==1, 'weights']))
    elif (year==2026) & (quarter==2):
        price.append( yb.loc[yb['years']==2026, 'Settlement Price'] * float(q_weights.loc[q_weights['quarters']==2, 'weights']))
    elif (year==2026) & (quarter==3):
        price.append( yb.loc[yb['years']==2026, 'Settlement Price'] * float(q_weights.loc[q_weights['quarters']==3, 'weights']))
    elif (year==2026) & (quarter==4):
        price.append( yb.loc[yb['years']==2026, 'Settlement Price'] * float(q_weights.loc[q_weights['quarters']==4, 'weights']))
    elif (year==2027) & (quarter==1):
        price.append( yb.loc[yb['years']==2027, 'Settlement Price'] * float(q_weights.loc[q_weights['quarters']==1, 'weights']))
    elif (year==2027) & (quarter==2):
        price.append( yb.loc[yb['years']==2027, 'Settlement Price'] * float(q_weights.loc[q_weights['quarters']==2, 'weights']))
    elif (year==2027) & (quarter==3):
        price.append( yb.loc[yb['years']==2027, 'Settlement Price'] * float(q_weights.loc[q_weights['quarters']==3, 'weights']))
    elif (year==2027) & (quarter==4):
        price.append( yb.loc[yb['years']==2027, 'Settlement Price'] * float(q_weights.loc[q_weights['quarters']==4, 'weights']))
    elif (year==2028) & (quarter==1):
        price.append( yb.loc[yb['years']==2028, 'Settlement Price'] * float(q_weights.loc[q_weights['quarters']==1, 'weights']))
    elif (year==2028) & (quarter==2):
        price.append( yb.loc[yb['years']==2028, 'Settlement Price'] * float(q_weights.loc[q_weights['quarters']==2, 'weights']))
    elif (year==2028) & (quarter==3):
        price.append( yb.loc[yb['years']==2028, 'Settlement Price'] * float(q_weights.loc[q_weights['quarters']==3, 'weights']))
    elif (year==2028) & (quarter==4):
        price.append( yb.loc[yb['years']==2028, 'Settlement Price'] * float(q_weights.loc[q_weights['quarters']==4, 'weights']))

qb_temp['Settlement Price']=[price[i].values[0] for i in range(len(price))]
frames=[qb, qb_temp]
prices_qb_ext=pd.concat(frames, axis=0, ignore_index=True)
prices_qb_ext.to_excel(path+'prices_qb.xlsx', index=False)

#=====================Months=================================
#Import quarterly prices to compute monthly prices
prices_qb=pd.read_excel(path+'prices_qb.xlsx')
qb=prices_qb.copy()

mb['Delivery Period']=pd.to_datetime(mb['Delivery Period'], format='%b/%y')

list_m=[]
date_start=mb['Delivery Period'][5]
for i in range(horizon_m): 
    date_start += pd.DateOffset(months=1)   
    list_m.append(date_start)

mb_temp = pd.DataFrame({'Delivery Period': list_m})
mb_temp =mb.append(mb_temp, ignore_index=True)

mb_temp['years']=mb_temp['Delivery Period'].dt.year
mb_temp['quarters']=mb_temp['Delivery Period'].dt.quarter
mb_temp['months']=mb_temp['Delivery Period'].dt.month

mb_=mb_temp.iloc[0:6,:]
mb_temp_=mb_temp.iloc[6:,]

price=[]
for idx, row in mb_temp_.iterrows():
    year=row['years']
    quarter=row['quarters']
    month=row['months']
    #2023
    if (year==2023) & (quarter==1) & (month==1):
        price.append(qb.loc[(qb['years']==2023) & (qb['quarters']==1), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==1, 'weight_m1']))      
    elif (year==2023) & (quarter==1) & (month==2):
        price.append(qb.loc[(qb['years']==2023) & (qb['quarters']==1), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==1, 'weight_m2']))
    elif (year==2023) & (quarter==1) & (month==3):
        price.append(qb.loc[(qb['years']==2023) & (qb['quarters']==1), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==1, 'weight_m3']))
    elif (year==2023) & (quarter==2) & (month==4):
        price.append(qb.loc[(qb['years']==2023) & (qb['quarters']==2), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==2, 'weight_m1']))
    elif (year==2023) & (quarter==2) & (month==5):
        price.append(qb.loc[(qb['years']==2023) & (qb['quarters']==2), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==2, 'weight_m2']))
    elif (year==2023) & (quarter==2) & (month==6):
        price.append(qb.loc[(qb['years']==2023) & (qb['quarters']==2), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==2, 'weight_m3']))
    elif (year==2023) & (quarter==3) & (month==7):
        price.append(qb.loc[(qb['years']==2023) & (qb['quarters']==3), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==3, 'weight_m1']))
    elif (year==2023) & (quarter==3) & (month==8):
        price.append(qb.loc[(qb['years']==2023) & (qb['quarters']==3), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==3, 'weight_m2']))
    elif (year==2023) & (quarter==3) & (month==9):
        price.append(qb.loc[(qb['years']==2023) & (qb['quarters']==3), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==3, 'weight_m3']))
    elif (year==2023) & (quarter==4) & (month==10):
        price.append(qb.loc[(qb['years']==2023) & (qb['quarters']==4), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==4, 'weight_m1']))
    elif (year==2023) & (quarter==4) & (month==11):
        price.append(qb.loc[(qb['years']==2023) & (qb['quarters']==4), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==4, 'weight_m2']))
    elif (year==2023) & (quarter==4) & (month==12):
        price.append(qb.loc[(qb['years']==2023) & (qb['quarters']==4), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==4, 'weight_m3']))
    #2024
    elif (year==2024) & (quarter==1) & (month==1):
        price.append(qb.loc[(qb['years']==2024) & (qb['quarters']==1), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==1, 'weight_m1']))
    elif (year==2024) & (quarter==1) & (month==2):
        price.append(qb.loc[(qb['years']==2024) & (qb['quarters']==1), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==1, 'weight_m2']))
    elif (year==2024) & (quarter==1) & (month==3):
        price.append(qb.loc[(qb['years']==2024) & (qb['quarters']==1), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==1, 'weight_m3']))
    elif (year==2024) & (quarter==2) & (month==4):
        price.append(qb.loc[(qb['years']==2024) & (qb['quarters']==2), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==2, 'weight_m1']))
    elif (year==2024) & (quarter==2) & (month==5):
        price.append(qb.loc[(qb['years']==2024) & (qb['quarters']==2), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==2, 'weight_m2']))
    elif (year==2024) & (quarter==2) & (month==6):
        price.append(qb.loc[(qb['years']==2024) & (qb['quarters']==2), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==2, 'weight_m3']))
    elif (year==2024) & (quarter==3) & (month==7):
        price.append(qb.loc[(qb['years']==2024) & (qb['quarters']==3), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==3, 'weight_m1']))
    elif (year==2024) & (quarter==3) & (month==8):
        price.append(qb.loc[(qb['years']==2024) & (qb['quarters']==3), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==3, 'weight_m2']))
    elif (year==2024) & (quarter==3) & (month==9):
        price.append(qb.loc[(qb['years']==2024) & (qb['quarters']==3), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==3, 'weight_m3']))
    elif (year==2024) & (quarter==4) & (month==10):
        price.append(qb.loc[(qb['years']==2024) & (qb['quarters']==4), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==4, 'weight_m1']))
    elif (year==2024) & (quarter==4) & (month==11):
        price.append(qb.loc[(qb['years']==2024) & (qb['quarters']==4), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==4, 'weight_m2']))
    elif (year==2024) & (quarter==4) & (month==12):
        price.append(qb.loc[(qb['years']==2024) & (qb['quarters']==4), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==4, 'weight_m3']))
    #2025
    elif (year==2025) & (quarter==1) & (month==1):
        price.append(qb.loc[(qb['years']==2025) & (qb['quarters']==1), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==1, 'weight_m1']))
    elif (year==2025) & (quarter==1) & (month==2):
        price.append(qb.loc[(qb['years']==2025) & (qb['quarters']==1), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==1, 'weight_m2']))
    elif (year==2025) & (quarter==1) & (month==3):
        price.append(qb.loc[(qb['years']==2025) & (qb['quarters']==1), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==1, 'weight_m3']))
    elif (year==2025) & (quarter==2) & (month==4):
        price.append(qb.loc[(qb['years']==2025) & (qb['quarters']==2), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==2, 'weight_m1']))
    elif (year==2025) & (quarter==2) & (month==5):
        price.append(qb.loc[(qb['years']==2025) & (qb['quarters']==2), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==2, 'weight_m2']))
    elif (year==2025) & (quarter==2) & (month==6):
        price.append(qb.loc[(qb['years']==2025) & (qb['quarters']==2), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==2, 'weight_m3']))
    elif (year==2025) & (quarter==3) & (month==7):
        price.append(qb.loc[(qb['years']==2025) & (qb['quarters']==3), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==3, 'weight_m1']))
    elif (year==2025) & (quarter==3) & (month==8):
        price.append(qb.loc[(qb['years']==2025) & (qb['quarters']==3), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==3, 'weight_m2']))
    elif (year==2025) & (quarter==3) & (month==9):
        price.append(qb.loc[(qb['years']==2025) & (qb['quarters']==3), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==3, 'weight_m3']))
    elif (year==2025) & (quarter==4) & (month==10):
        price.append(qb.loc[(qb['years']==2025) & (qb['quarters']==4), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==4, 'weight_m1']))
    elif (year==2025) & (quarter==4) & (month==11):
        price.append(qb.loc[(qb['years']==2025) & (qb['quarters']==4), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==4, 'weight_m2']))
    elif (year==2025) & (quarter==4) & (month==12):
        price.append(qb.loc[(qb['years']==2025) & (qb['quarters']==4), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==4, 'weight_m3']))
    #2026
    elif (year==2026) & (quarter==1) & (month==1):
        price.append(qb.loc[(qb['years']==2026) & (qb['quarters']==1), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==1, 'weight_m1']))
    elif (year==2026) & (quarter==1) & (month==2):
        price.append(qb.loc[(qb['years']==2026) & (qb['quarters']==1), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==1, 'weight_m2']))
    elif (year==2026) & (quarter==1) & (month==3):
        price.append(qb.loc[(qb['years']==2026) & (qb['quarters']==1), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==1, 'weight_m3']))
    elif (year==2026) & (quarter==2) & (month==4):
        price.append(qb.loc[(qb['years']==2026) & (qb['quarters']==2), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==2, 'weight_m1']))
    elif (year==2026) & (quarter==2) & (month==5):
        price.append(qb.loc[(qb['years']==2026) & (qb['quarters']==2), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==2, 'weight_m2']))
    elif (year==2026) & (quarter==2) & (month==6):
        price.append(qb.loc[(qb['years']==2026) & (qb['quarters']==2), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==2, 'weight_m3']))
    elif (year==2026) & (quarter==3) & (month==7):
        price.append(qb.loc[(qb['years']==2026) & (qb['quarters']==3), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==3, 'weight_m1']))
    elif (year==2026) & (quarter==3) & (month==8):
        price.append(qb.loc[(qb['years']==2026) & (qb['quarters']==3), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==3, 'weight_m2']))
    elif (year==2026) & (quarter==3) & (month==9):
        price.append(qb.loc[(qb['years']==2026) & (qb['quarters']==3), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==3, 'weight_m3']))
    elif (year==2026) & (quarter==4) & (month==10):
        price.append(qb.loc[(qb['years']==2026) & (qb['quarters']==4), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==4, 'weight_m1']))
    elif (year==2026) & (quarter==4) & (month==11):
        price.append(qb.loc[(qb['years']==2026) & (qb['quarters']==4), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==4, 'weight_m2']))
    elif (year==2026) & (quarter==4) & (month==12):
        price.append(qb.loc[(qb['years']==2026) & (qb['quarters']==4), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==4, 'weight_m3']))
    #2027
    elif (year==2027) & (quarter==1) & (month==1):
        price.append(qb.loc[(qb['years']==2027) & (qb['quarters']==1), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==1, 'weight_m1']))
    elif (year==2027) & (quarter==1) & (month==2):
        price.append(qb.loc[(qb['years']==2027) & (qb['quarters']==1), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==1, 'weight_m2']))
    elif (year==2027) & (quarter==1) & (month==3):
        price.append(qb.loc[(qb['years']==2027) & (qb['quarters']==1), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==1, 'weight_m3']))
    elif (year==2027) & (quarter==2) & (month==4):
        price.append(qb.loc[(qb['years']==2027) & (qb['quarters']==2), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==2, 'weight_m1']))
    elif (year==2027) & (quarter==2) & (month==5):
        price.append(qb.loc[(qb['years']==2027) & (qb['quarters']==2), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==2, 'weight_m2']))
    elif (year==2027) & (quarter==2) & (month==6):
        price.append(qb.loc[(qb['years']==2027) & (qb['quarters']==2), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==2, 'weight_m3']))
    elif (year==2027) & (quarter==3) & (month==7):
        price.append(qb.loc[(qb['years']==2027) & (qb['quarters']==3), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==3, 'weight_m1']))
    elif (year==2027) & (quarter==3) & (month==8):
        price.append(qb.loc[(qb['years']==2027) & (qb['quarters']==3), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==3, 'weight_m2']))
    elif (year==2027) & (quarter==3) & (month==9):
        price.append(qb.loc[(qb['years']==2027) & (qb['quarters']==3), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==3, 'weight_m3']))
    elif (year==2027) & (quarter==4) & (month==10):
        price.append(qb.loc[(qb['years']==2027) & (qb['quarters']==4), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==4, 'weight_m1']))
    elif (year==2027) & (quarter==4) & (month==11):
        price.append(qb.loc[(qb['years']==2027) & (qb['quarters']==4), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==4, 'weight_m2']))
    elif (year==2027) & (quarter==4) & (month==12):
        price.append(qb.loc[(qb['years']==2027) & (qb['quarters']==4), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==4, 'weight_m3']))
    #2028
    elif (year==2028) & (quarter==1) & (month==1):
        price.append(qb.loc[(qb['years']==2028) & (qb['quarters']==1), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==1, 'weight_m1']))
    elif (year==2028) & (quarter==1) & (month==2):
        price.append(qb.loc[(qb['years']==2028) & (qb['quarters']==1), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==1, 'weight_m2']))
    elif (year==2028) & (quarter==1) & (month==3):
        price.append(qb.loc[(qb['years']==2028) & (qb['quarters']==1), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==1, 'weight_m3']))
    elif (year==2028) & (quarter==2) & (month==4):
        price.append(qb.loc[(qb['years']==2028) & (qb['quarters']==2), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==2, 'weight_m1']))
    elif (year==2028) & (quarter==2) & (month==5):
        price.append(qb.loc[(qb['years']==2028) & (qb['quarters']==2), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==2, 'weight_m2']))
    elif (year==2028) & (quarter==2) & (month==6):
        price.append(qb.loc[(qb['years']==2028) & (qb['quarters']==2), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==2, 'weight_m3']))
    elif (year==2028) & (quarter==3) & (month==7):
        price.append(qb.loc[(qb['years']==2028) & (qb['quarters']==3), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==3, 'weight_m1']))
    elif (year==2028) & (quarter==3) & (month==8):
        price.append(qb.loc[(qb['years']==2028) & (qb['quarters']==3), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==3, 'weight_m2']))
    elif (year==2028) & (quarter==3) & (month==9):
        price.append(qb.loc[(qb['years']==2028) & (qb['quarters']==3), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==3, 'weight_m3']))
    elif (year==2028) & (quarter==4) & (month==10):
        price.append(qb.loc[(qb['years']==2028) & (qb['quarters']==4), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==4, 'weight_m1']))
    elif (year==2028) & (quarter==4) & (month==11):
        price.append(qb.loc[(qb['years']==2028) & (qb['quarters']==4), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==4, 'weight_m2']))
    elif (year==2028) & (quarter==4) & (month==12):
        price.append(qb.loc[(qb['years']==2028) & (qb['quarters']==4), 'Settlement Price']*float(m_weights.loc[m_weights['quarters']==4, 'weight_m3']))
    

mb_temp_['Settlement Price']=[price[i].values[0] for i in range(len(price))]
frames=[mb_, mb_temp_]
prices_mb_ext=pd.concat(frames, axis=0, ignore_index=True)
scrapped_date=(datetime.now()).strftime("%y_%m_%d")
yesterday=(datetime.today() - timedelta(days=1)).strftime("%y_%m_%d") 
prices_mb_ext.to_excel(path+'prices_mb.xlsx', index=False, sheet_name=f"mb_{prices_mb_ext['Date'][0]}_scrapped_{scrapped_date}")

#======================================================
#=========== Load price curve in DB  ==================
#======================================================

prices_mb_ext['cotation_date']=prices_mb_ext['Date'][0]
prices_mb_ext_=prices_mb_ext[['Delivery Period', 'Settlement Price', 'cotation_date']]
prices_mb_ext_.rename(columns = {"Delivery Period":"delivery_period", "Settlement Price":"settlement_price", 
                     }, inplace = True)


def open_database():
    print('Connecting to SQL Server with ODBC driver')
    connection_string = 'DRIVER={SQL Server};SERVER='+server_credentials['server']+';DATABASE='+server_credentials['database']+';UID='+server_credentials['username']+';Trusted_Connection='+server_credentials['yes']
    cnxn = pyodbc.connect(connection_string)
    print('connected!')

    return cnxn

#windows authentication 
def mssql_engine(): 
    engine = create_engine('mssql+pyodbc://BLX186-SQ1PRO01/StarDust?driver=SQL+Server+Native+Client+11.0',
                           fast_executemany=True) 
    return engine
cnx=open_database()
cursor = cnx.cursor()

for index, row in prices_mb_ext_.iterrows():
    cursor.execute("INSERT INTO market_prices_fr_eex (delivery_period, settlement_price, cotation_date) values(?, ?, ?)", 
                   row.delivery_period, row.settlement_price, row.cotation_date)
cnx.commit()