from sheetfu import SpreadsheetApp
import os
import pandas as pd
import requests
import urllib.request
import time
from datetime import date
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import csv

#function for getting current USD/EUR rate of change 
def getrate(exchangelink):
    r = requests.get(exchangelink) #request page access
    soup = BeautifulSoup(r.text, 'html.parser')  #parse through html
    data = soup.findAll("td") #find td
    datapoint = str(data[1])  #get the needed exchange rate
    rate = float(datapoint[4:-5]) #transform it to float
    return rate

#function for converting from days to date
def serial_date_to_string(srl_no):
    new_date = datetime.datetime(1900,1,1,0,0) + datetime.timedelta(srl_no - 2)
    return new_date.strftime("%Y/%m/%d")

#function for reading from google spreadsheets
def readingfromgoogle(serviceaccountfile, googleid, sheetname):
    spreadsheet = SpreadsheetApp(serviceaccountfile).open_by_id(googleid)
    sheet = spreadsheet.get_sheet_by_name(sheetname) #access the wanted tab
    data_range = sheet.get_data_range()                 #extract range where the data is
    values = data_range.get_values()                    #get values
    values = pd.DataFrame(data = values[8:], columns = values[7]) #put the data into pandas dataframe
    excel = False
    return values, excel

#function for reading from excel
def readingfromexcel(dataset, sheetname):
    values = pd.read_excel(dataset, sheetname, header = 7, names = ["Advertiser", "Placement", "Date", "Total impressions", "Revenue (€)", "Date","Advertisers","Key-values ID","Total impressions","Revenue (€)","Date","Advertisers","Key-values ID","Total impressions","Revenue (€)","Date","Advertisers","Key-values ID","Total impressions","Revenue (USD)"])
    values.columns = ['Advertiser', 'Placement', 'Date', 'Total impressions', 'Revenue (€)',
       'Date', 'Advertisers', 'Key-values ID', 'Total impressions',
       'Revenue (€)', 'Date', 'Advertisers', 'Key-values ID',
       'Total impressions', 'Revenue (€)', 'Date', 'Advertisers',
       'Key-values ID', 'Total impressions', 'Revenue (USD)']
    excel = True
    return values, excel

#transforming dataset
def transformdata(values, rate):
    values["Revenue (USD)"] = values["Revenue (USD)"].apply(lambda x: x/rate)
    values.rename(columns = {'Revenue (USD)':'Revenue (€)'}, inplace = True)
    values.rename(columns = {'Advertiser':'Advertisers'}, inplace = True)
    values.insert(7, "Placement", ["MM_BPCOM_HBS_Placement" for i in range(len(values))], True)
    values.insert(13, "Placement", ["MM_BPES_HBS_Placement" for i in range(len(values))], True)
    values.insert(19, "Placement", ["MM_DE_HBS_Placement" for i in range(len(values))], True)
    return values

#joining 4 datasets
def concatdata(values, excel):
    df1 = values.iloc[:, 0:5]
    df2 = values.iloc[:, 5:11]
    df3 = values.iloc[:, 11:17]
    df4 = values.iloc[:, 17:23]
    values = pd.concat([df1, df2, df3, df4])
    values = values.reset_index(inplace = True)
    if excel == False:
        values["Date"] = [serial_date_to_string(int(i)) for i in values["Date"] if i != "Date"]
    return values

#saving transformed and joined data to excel
def savejoineddata(values, name):
    values.to_excel(name, columns = ["Advertisers", "Placement", "Date", "Total impressions", "Revenue (€)", "Key-values ID"])

#creating a table of revenue against advertisers
def summarytable(values):
    adsvsrev = values[["Advertisers", "Revenue (€)"]].groupby("Advertisers").sum().sort_values(by=["Revenue (€)"])
    allrevenue = adsvsrev["Revenue (€)"].sum()
    adsvsrev["Revenue (€)"] = adsvsrev["Revenue (€)"].apply(lambda x: (x/allrevenue)*100)
    adsvsrev.rename(columns = {'Revenue (€)':'Revenue, %'}, inplace = True)
    adsvsrev = adsvsrev.reset_index()
    adsvsrev.to_excel("summary table.xlsx", columns = ["Advertisers", 'Revenue, %'])
    return adsvsrev

#summary pie chart
def summarypiechart(asdvsrev):
    fig1, ax1 = plt.subplots(figsize=(8, 6))

    ax1.pie(adsvsrev['Revenue, %'], labels=adsvsrev['Advertisers'], autopct=None,
            shadow=True, radius = 5, labeldistance = None, startangle=90, rotatelabels = True)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    total = sum(adsvsrev['Revenue, %'])
    plt.legend(
        loc='upper left',
        labels=['%s, %1.1f%%' % (
            l, (float(s) / total) * 100) for l, s in zip(adsvsrev['Advertisers'], adsvsrev['Revenue, %'])],
        prop={'size': 8},
        bbox_to_anchor=(0.0, 1),
        bbox_transform=fig1.transFigure
    )
    plt.title("Percentage of Revenue against Advertisers")
    plt.savefig("summary graph.png")
    
cols = ["Advertisers", "Placement", "Date", "Total impressions", "Revenue (€)", "Key-values ID"]
dataset = "dataset.xlsx"
sheetname = "Raw Report"
exchangelink = "https://www.xe.com/currencycharts/?from=USD&to=EUR"
serviceaccountfile = "input your own .json file here"
googleid = "input the google id"
name = "concatenated.xlsx"  

#values, excel = readingfromgoogle(serviceaccountfile, googleid, sheetname)
values, excel = readingfromexcel(dataset, sheetname)
rate = getrate(exchangelink)
values = transformdata(values, rate)
values = concatdata(values, excel)
