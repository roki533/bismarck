import os
import pandas as pd

from apps.app import app

def api_upload(machine_id, df_cash):

    # machine_idを付加して、DBに書き込む
    # 重複データは上書きする

    # ここでは、固定のテスト用のcsvファイルをDBに登録する

    df_cash = pd.read_csv("./bnp/986027.csv")

    # 先頭に装置番号を追加
    df_cash.insert(loc = 0, column= 'machine_id', value= machine_id)

    df_cash.rename(columns={'time': 'date', '100k': 'cur1', '50k': 'cur2'}, inplace=True)

    #print(df_cash)
    # 
    SQLALCHEMY_DATABASE_URI = app.config['SQLALCHEMY_DATABASE_URI']

    df = pd.read_sql('cash', SQLALCHEMY_DATABASE_URI)
    print(df)

    #SQLALCHEMY_DATABASE_URI = f"sqlite:///{'D:/資金予測/cashopt/local.sqlite'}"
    df_cash.to_sql('cash', SQLALCHEMY_DATABASE_URI, if_exists='append', index=False)

    df = pd.read_sql('cash', SQLALCHEMY_DATABASE_URI)
    print(df)

    return 
