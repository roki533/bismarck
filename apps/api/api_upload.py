import pandas as pd

from apps.app import app
from apps.app import db
from apps.crud.models import Cash

# ファイルをアップロードする
def api_upload(machine_id, request):
    """
    構造化されたEJデータファイルをDBに書き込む

    Args:
        machine_id (str): 装置ID
        request(request) : HTTPリクエスト

    Returns:
        なし
    Note:
        リクエスト

        'POST' \
        'http://127.0.0.1:5000/api/data/ws0001' \  
        -H 'accept: application/json' \  
        -H 'Content-Type: multipart/form-data' \  
        -F 'file=@986027.csv;type=text/csv'  

    """

    # アップロードファイルのデータ
    file = request.files['file']

    # ファイル読み込み
    df_cash = pd.read_csv(file)

    # 先頭に装置番号を追加
    df_cash.insert(loc = 0, column= 'machine_id', value= machine_id)

    # 金種名を変更しておく(これは再考必要)
    # アップロード時に変更しているためだが、元のアップロードデータを変更するのが良い
    df_cash.rename(columns={'time': 'date', '100k': 'cur1', '50k': 'cur2'}, inplace=True)

    # DBの設定読み込み
    SQLALCHEMY_DATABASE_URI = app.config['SQLALCHEMY_DATABASE_URI']

    # 現状のmachine_idのDBデータを読み込む
    text = "SELECT * FROM cash WHERE machine_id ='" + machine_id + "'"
    df = pd.read_sql_query(sql = text, con=SQLALCHEMY_DATABASE_URI)
    df.drop(['id'], axis=1, inplace=True) # idを削除

    # アップロードしたデータと結合
    df = pd.concat([df,df_cash])

    # 重複行は削除する。アップロードデータは残す
    df = df.drop_duplicates(subset=['machine_id', 'date'],keep='last')

    # machine_idのDBデータを一旦削除
    del_cash = db.session.query(Cash).filter(Cash.machine_id==machine_id).delete()
    db.session.commit()

    # 新たにDBに書き込む
    df.to_sql('cash', SQLALCHEMY_DATABASE_URI, if_exists='append', index=False)

    print('api_upload() : DB書き込みデータ\n',df.head())

    # DB書き込みのテスト
    #df = pd.read_sql('cash', SQLALCHEMY_DATABASE_URI)
    #print(df)

    return 


