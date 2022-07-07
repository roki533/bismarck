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



from flask import Flask, request, make_response, jsonify
import os
import werkzeug
import base64
from datetime import datetime


# 環境変数からデータサイズ（単位はByte）を制限する
# limit upload file size : 1MB
# ex) set MAX_JSON_CONTENT_LENGTH=1048576
MAX_JSON_CONTENT_LENGTH = int(os.getenv("MAX_JSON_CONTENT_LENGTH", default="0"))

# アップロードされたファイルの場所
# ex) set UPLOAD_DIR_PATH=C:/tmp/flaskUploadDir
UPLOAD_DIR = os.getenv("UPLOAD_DIR_PATH")

def api_upload2(machine_id, df_cash):

    # machine_idを付加して、DBに書き込む
    # 重複データは上書きする

    # request.jsonで送信されたデータをjsonとしてアクセスする
    jsonData = request.json
    fileName = jsonData.get("fileName")
    contentType = jsonData.get("contentType")
    contentDataAscii = jsonData.get("contentData")

    # バイナリデータにデコード
    contentData = base64.b64decode(contentDataAscii)

    # アップロードされたファイルのデータサイズが超過していないかチェック
    contentDataSize = len(contentData)
    if MAX_JSON_CONTENT_LENGTH > 0:
        if MAX_JSON_CONTENT_LENGTH < contentDataSize:
            raise werkzeug.exceptions.RequestEntityTooLarge( \
                "json content length over : {0}".format(contentDataSize))

    # 取得したバイナリデータをファイルとして保存
    saveFileName = datetime.now().strftime("%Y%m%d_%H%M%S_") \
        + werkzeug.utils.secure_filename(fileName)
    with open(os.path.join(UPLOAD_DIR, saveFileName), 'wb') as saveFile:
        saveFile.write(contentData)

    return

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

# 超過したファイルの例外処理
@app.errorhandler(werkzeug.exceptions.RequestEntityTooLarge)
def handle_over_max_file_size(error):
    print("werkzeug.exceptions.RequestEntityTooLarge")
    return 'result : file size is overed.'
