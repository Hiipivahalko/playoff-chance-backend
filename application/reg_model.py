import numpy as np
import pandas as pd
import random
import requests
import json
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

REG_MODEL= None

def build_model():

    data_path = f'{dir_path}/data'

    #drive.mount('/content/drive')
    dataDict = {}
    for year in range(1992,2021):
        if year == 2004:
            continue
        nextYear = year + 1
        nextYear = str(nextYear)
        nextYear = nextYear[2:]
        data = pd.read_csv(f'{data_path}/NHL_Data/{str(year)}-{nextYear}.csv')
        dataDict[year] = data


######

    #Combine all the individual season data frames into one
    allData = pd.concat(dataDict.values() ,axis=0)
    #Remove unnecessary columns that won't be used as features in the model
    allData.drop(['W', 'L', 'T', 'OT', 'P', 'GP', 'P%', 'RW', 'ROW', 'S/O Win', 'GF', 'GA'], axis=1, inplace=True)
    #allData.head()

######

    fowValues = []
    for year in range(1997,2021):
        if year == 2004:
            continue
        nextYear = year + 1
        season = allData.loc[allData['Season'] == int((str(year) + str(nextYear)))]
        fowValues.append((round(season.median()['FOW%'], 1)))

    #Fill empty values with a median FOW% result from another season
    allData=allData.replace(to_replace = '--', value = random.choice(fowValues))
    #allData.head()


######

    #import goalies data
    goaliesDict={}
    star_goaliesDict = {}
    for year in range(1992,2021):
        if year == 2004:
            continue
        nextYear = year + 1
        nextYear = str(nextYear)
        nextYear = nextYear[2:]
        data = pd.read_excel(f'{data_path}/goalies/{str(year)}-{nextYear}.xlsx')
        #Fill empty values with 0
        data=data.replace(to_replace = '--', value = 0)
        #GAA's value was adjusted to the same value range as Sv% [0,1] 
        data.GAA=data.GAA/data.GAA.max()
        #Sv% is positive for goalie and GAA is negtive, goalie performance consider equal weight of each feature
        data['goalie_performance']=data['Sv%']-data.GAA
        #sorted by goalie performance and keep first ten as star players 
        data=data.sort_values(by='goalie_performance',ascending=False)
        data=data.reset_index(drop=True)
        #drop unnecessary columns that won't be used as features in the model
        data.drop(['S/C', 'GP', 'GS', 'W', 'L', 'T', 'OT','SA', 'Svs', 'GA', 'Sv%', 'GAA', 'TOI', 'SO', 'G', 'A', 'P', 'PIM'], axis=1, inplace=True)
        star_goalies=data.iloc[0:10]
        goaliesDict[year]=data
        star_goaliesDict[year] =star_goalies
    #Combine all the individual season data frames into one
    all_star_goalies = pd.concat(star_goaliesDict.values() ,axis=0)
    all_goalies= pd.concat(goaliesDict.values() ,axis=0)
    #print(all_star_goalies.shape)
    #print(all_goalies.shape)

#######


    #import skaters data
    all_skatersDict = {}
    for year in range(1992,2021):
        if year == 2004:
            continue
        nextYear = year + 1
        nextYear = str(nextYear)
        nextYear = nextYear[2:]
        oneseasonDict={}
    #oneseason's data are saved in seperate xlsx file, then use for loop to combine them
        for i in range(1,11):
            try:
                oneseasonDict[i] = pd.read_excel(f'{data_path}/skaters/{str(year)}-{nextYear}/{i}.xlsx')
            except:
                continue
        #Combine all the individual data sheets frames into one
        oneseason=pd.concat(oneseasonDict.values() ,axis=0)
    
        all_skatersDict[year]= pd.concat(oneseasonDict.values() ,axis=0)

    #get Defensemen performance data of Defense skaters and obtain star defensers roster
    defenseDict={}
    star_defenseDict = {}
    for year in range(1992,2021):
        if year == 2004:
            continue
        data = all_skatersDict[year]
        data=data[data.Pos=='D']
        #Fill empty values with 0
        data=data.replace(to_replace = '--', value = 0)
        data.drop(['S/C', 'Pos', 'GP', 'A', 'P','EVG', 'EVP', 'PPG', 'PPP', 'SHG', 'SHP', 'OTG', 'GWG','TOI/GP', 'FOW%'], axis=1, inplace=True)
        # Defensemen performance combine skaters features status of (+/-), points per game, PIM, goals, shots, shots%, all the features values are set in [0,1] and handle in equal weight
        data.G=data.G/data.G.max()
        data['+/-']=data['+/-']/data['+/-'].max()
        data.PIM=data.PIM/data.PIM.max()
        data['P/GP']=data['P/GP']/data['P/GP'].max()
        data['S']=data['S']/data['S'].max()
        data['S%'] = pd.to_numeric(data['S%'],errors='coerce')
        data['S%']=data['S%']/data['S%'].max()
        data['Defense']=data.G+data['+/-']+data.PIM+data['P/GP']+data['S']+ data['S%']
        #sorted by defense performance and keep first 20 each season as star players 
        data=data.sort_values(by='Defense',ascending=False)
        data=data.reset_index(drop=True)
        star_defense=data.iloc[0:20]
        defenseDict[year]=data
        star_defenseDict[year] =star_defense

    #get forward performance data of forward skaters and obtain star forwarder's roster
    forwardDict={}
    star_forwardDict = {}
    for year in range(1992,2021):
        if year == 2004:
            continue
        data = all_skatersDict[year]
        data=data[data.Pos!='D']
        #Fill empty values with 0
        data=data.replace(to_replace = '--', value = 0)
        data.drop(['S/C', 'Pos', 'GP', 'A', 'P','EVG', 'EVP', 'PPG', 'PPP', 'SHG', 'SHP', 'OTG', 'GWG','TOI/GP', 'FOW%'], axis=1, inplace=True)
        # forward performance combine skaters features status of(+/-), points per game, PIM, goals, shots, shots%, all the features values are set in [0,1] and handle them in equal weight
        data.G=data.G/data.G.max()
        data['+/-']=data['+/-']/data['+/-'].max()
        data.PIM=data.PIM/data.PIM.max()
        data['P/GP']=data['P/GP']/data['P/GP'].max()
        data['S']=data['S']/data['S'].max()
        data['S%'] = pd.to_numeric(data['S%'],errors='coerce')
        data['S%']=data['S%']/data['S%'].max()
        data['Forward']=data.G+data['+/-']+data.PIM+data['P/GP']+data['S']+ data['S%']
        #sorted by forward performance and keep first 20 each season as star players 
        data=data.sort_values(by='Forward',ascending=False)
        data=data.reset_index(drop=True)
        star_forward=data.iloc[0:20]
        forwardDict[year]=data
        star_forwardDict[year] =star_forward

    #combine gollies, defense performance and forward performance of skaters by teams
    skatersDict={}
    for year in range(1992,2021):
        if year == 2004:
            continue
        skaters=pd.concat([forwardDict[year],defenseDict[year],goaliesDict[year]],axis=0)
        skaters.drop(['+/-', 'G', 'P/GP', 'S','S%'], axis=1, inplace=True)
        skaters=skaters.fillna(0)
        skaters_manyteam=pd.DataFrame()
        #skaters belong to two or three teams, copy his performance for each team, then calculate team's average performance
        for i in skaters.Team.unique():
            if len(i)>6:
                j=i.split(',')
                r2=skaters.loc[skaters.Team==i]
                r3=skaters.loc[skaters.Team==i]
                skaters['Team'].replace({i: j[0]}, inplace=True)
                r2['Team'].replace({i: j[1]}, inplace=True)
                skaters_manyteam=skaters_manyteam.append(r2)
                try:
                    r3['Team'].replace({i: j[2]}, inplace=True) 
                    skaters_manyteam=skaters_manyteam.append(r3)
                except:
                    continue      
        skaters=skaters.append(skaters_manyteam)
        skatersDict[year]=skaters.groupby(['Team']).mean()
    #skatersDict[1992]


#########


    for year in range(1992,2021):
        if year == 2004:
            continue
        star_player=pd.concat([star_goaliesDict[year],star_defenseDict[year],star_forwardDict[year]],axis=0)
        starskaters_manyteam=pd.DataFrame()
        #skaters belong to two or three teams, the number of star players should caluculated for each team separately.
        for i in star_player.Team.unique():
            if len(i)>6:
                j=i.split(',')
                r2=skaters.loc[skaters.Team==i]
                r3=skaters.loc[skaters.Team==i]
                star_player['Team'].replace({i: j[0]}, inplace=True)
                r2['Team'].replace({i: j[1]}, inplace=True)
                starskaters_manyteam=starskaters_manyteam.append(r2)
                try:
                   r3['Team'].replace({i: j[2]}, inplace=True) 
                   starskaters_manyteam=starskaters_manyteam.append(r3)
                except:
                    continue 
        star_player=star_player.append(starskaters_manyteam)
        star=star_player.Team.to_numpy()
        for i in np.unique(star):
            skatersDict[year].loc[i,'star_player']=np.sum(star==i)
    skaters_performance_perteam= pd.concat(skatersDict.values() ,axis=0)
    skaters_performance_perteam=skaters_performance_perteam.reset_index()


####


    teamname={}
    for i in range(1,56):
        sub_req = "https://statsapi.web.nhl.com/api/v1/teams/"+str(i)
        sub_r = requests.get(sub_req)
        team_json = sub_r.text
        team_data = json.loads(team_json)
        abbre=team_data['teams'][0]['abbreviation']
        name=team_data['teams'][0]['name']
        teamname[abbre]=name
    #replace teams name from abbreviation to whole name
    skaters_performance_perteam['Team'].replace(teamname, inplace=True)
    #skaters_performance_perteam.head


#######

    #combine skaters and teams dataframe
    team_data=pd.merge(skaters_performance_perteam,allData,on=['Team','Season'])
    team_data.drop(['Unnamed: 0'], axis=1, inplace=True)
    team_data=team_data.fillna(0)
    team_data=team_data.replace(to_replace = '--', value = 0)
    #team_data.head()


######

    X=team_data[['PIM', 'Forward', 'Defense', 'goalie_performance',\
       'star_player', 'GF/GP', 'GA/GP', 'PP%', 'PK%', 'Net PP%', 'Net PK%',\
       'Shots/GP', 'SA/GP', 'FOW%']]
    y=team_data['Playoff']
    X_train, X_test, y_train, y_test = train_test_split( X, y, test_size=0.2, random_state=0)
    logreg = LogisticRegression(max_iter=10000)
    logreg.fit(X_train, y_train)
    y_pred = logreg.predict(X_test)
    acc=accuracy_score(y_test, y_pred)
    #print("Accuracy %2.3f" % acc)

    return logreg


def build_and_set_model():
    global REG_MODEL
    REG_MODEL = build_model()
    print('###### ML REGRESSION_MODEL builded and set up ######')
    


