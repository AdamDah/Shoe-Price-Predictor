import PySimpleGUI as sg
import pandas as pd
import numpy as np
import datetime as dt
from sklearn.tree import DecisionTreeRegressor

df = pd.read_csv("scraped_data_final.csv",index_col=False)
df.pop("Unnamed: 0")
df['Order Date']= pd.to_datetime(df['Order Date'])
df['Release Date']= pd.to_datetime(df['Release Date'])
preds = []

sg.theme('DarkAmber')   # Add a little color to your windows
# All the stuff inside your window. This is the PSG magic code compactor...
layout = [[sg.Text('Hello and welcome to the sneaker price predictor')],
          [sg.Text('Please select the characteristics of the shoe you aim to sell and we will tell you the most accurate price')],
          [sg.Text('Brand'), sg.Combo(values=list(df["Brand"].unique()), size=(35,30), key='key Brand')],
          [sg.Text('Model'), sg.Combo(values=list(df["Sneaker Name"].unique()), size=(35,30), key='key Sneaker Name')],
          [sg.Text('Region'), sg.Combo(values=list(df["Buyer Region"].unique()), size=(35, 30), key='key Buyer Region')],
          [sg.Text('Shoe Size'), sg.Combo(values=list(df["Shoe Size"].unique()), size=(35, 30), key='key Shoe Size')],
          [sg.Text('Color'), sg.Combo(values=list(df["Colors"].unique()), size=(35, 30), key='key Colors')],
          [sg.B("PREDICT THE SELL PRICE", key = "launch_pred")],
          [sg.Text('Here is your preediction : ',key = "key_pred_1", visible=False), sg.T("", key = "key_pred_2")]]

# Create the Window
window = sg.Window('sneaker price predictor', layout)
# Event Loop to process "events"
while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Cancel'):
        break
    if event is "launch_pred":
        preds = []
        modalities = ["Brand","Sneaker Name","Buyer Region","Shoe Size","Colors"]
        for mod in modalities:
            df_ts = df[df[mod] == values["key "+mod]].groupby("Order Date").mean()[
                "Sale Price"].reset_index()
            df_ts = df_ts.rename(columns={"Order Date": "Order_Date", "Sale Price": "Sale_Price"})
            data_train = df_ts[df_ts.Order_Date < "2019-01-01"]
            data_test = df_ts[df_ts.Order_Date >= "2019-01-01"]
            data_train.Order_Date = data_train.Order_Date.map(dt.datetime.toordinal)
            X_train = data_train.Order_Date[:, np.newaxis]
            y_train = data_train.Sale_Price
            tree = DecisionTreeRegressor(criterion='squared_error', max_depth=10).fit(X_train, y_train)
            X_all = df_ts.Order_Date.map(dt.datetime.toordinal)[:, np.newaxis]
            pred_tree = tree.predict(X_all)
            preds.append(pred_tree[-1])
            window.update(values[""])


window.close()