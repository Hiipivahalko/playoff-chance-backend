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

    team_data = pd.read_csv(f'{data_path}/preprocessed_data.csv')

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
    


