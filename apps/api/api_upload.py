import os
import pandas as pd

from apps.app import app
from apps.app import db

from apps.crud.models import Cash


def api_upload(machine_id, request):

    # rest api : request.files with multipart/form-data
    # <form action="/data/upload" method="post" enctype="multipart/form-data">
    #   <input type="file" name="uploadfile"/>
    #   <input type="submit" value="submit"/>
    # </form>

    # アップロードファイルのデータ
    file = request.files['file']

    # machine ID
    #machine_id = request.form.get('machine_id')

    print("machine_id", machine_id)
    # ファイル読み込み
    df_cash = pd.read_csv(file)
    print(df_cash)

    # 先頭に装置番号を追加
    df_cash.insert(loc = 0, column= 'machine_id', value= machine_id)

    # 金種名を変更しておく
    df_cash.rename(columns={'time': 'date', '100k': 'cur1', '50k': 'cur2'}, inplace=True)


    SQLALCHEMY_DATABASE_URI = app.config['SQLALCHEMY_DATABASE_URI']

    # machine_idのDBデータを読み込む
    text = "SELECT * FROM cash WHERE machine_id ='" + machine_id + "'"
    df = pd.read_sql_query(sql = text, con=SQLALCHEMY_DATABASE_URI)
    df.drop(['id'], axis=1, inplace=True) # idを削除

    # アップロードデータと結合
    df = pd.concat([df,df_cash])

    # 重複行は削除する。アップロードデータは残す
    df = df.drop_duplicates(subset=['machine_id', 'date'],keep='last')

    # machine_idのDBデータを削除
    del_cash = db.session.query(Cash).filter(Cash.machine_id==machine_id).delete()
    db.session.commit()

    # DBに書き込む
    df.to_sql('cash', SQLALCHEMY_DATABASE_URI, if_exists='append', index=False)

    #df = pd.read_sql('cash', SQLALCHEMY_DATABASE_URI)
    #print(df)

    return 


    '''
    for i in range(len(df_cash)):
        dic = df_cash.iloc[i, :].to_dict()
        print(dic)
        if db.session.query(Cash).filter(Cash.machine_id==dic['machine_id'], Cash.date==dic['date']).update(dic) == 0:
            db.session.add(Cash(**dic))

    db.session.commit()
    '''


