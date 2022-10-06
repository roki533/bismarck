import pandas as pd
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta

from apps.app import app
from apps.app import db

import apps.api.settings as settings
from apps.crud.models import Train_result

from bnp.interface import bnp_train

def api_train(machine_id):
    """
    指定された装置IDの学習をおこなう。\n
    
    現時点では、学習対象データは、DB内のすべてのデータ(改善が必要)。\n
    テストデータは対象データの最終日からさかのぼって、\n
    設定TEST_MONTHで期間を指定している

    Args:
        machine_id (str): 装置ID

    Returns:
        train_resp (list): 学習結果のリスト

        [{
            currency (str) : 金種
            best_model_type (str) : ベストモデルタイプ
            mse_train (float) : 訓練のMSE
            mse_test (float) : テストのMSE
        }]
    Note:
        リクエスト

        'POST' \  
        'http://127.0.0.1:5000/api/models/ws0001' \  
        -H 'accept: application/json' \  
        -d ''

    """

    train_resp = []

    # データベースより、ATMIDのデータを読み込む
    SQLALCHEMY_DATABASE_URI = app.config['SQLALCHEMY_DATABASE_URI']

    text = "SELECT * FROM cash WHERE machine_id ='" + machine_id + "'"
    df = pd.read_sql_query(sql = text, con=SQLALCHEMY_DATABASE_URI)

    # データがあれば
    if not df.empty:
        # idとmachine_idを削除(id,machine_idはアップロード時に追加しているので)
        df.drop(['id', 'machine_id'], axis=1, inplace=True) 
        #print(df.head(3))
        #                      date  deposit  withdraw  cur1  ...      d     e    f    r
        #0      01/01/2021 00:06:05        1         0     0  ...  600.0  10.0  0.0  0.0
        #1      01/01/2021 00:10:14        0         1     4  ...  600.0  10.0  0.0  0.0
        #2      01/01/2021 00:10:48        0         1     1  ...  600.0  10.0  0.0  0.0

        # データの開始日と終了日
        # 最初の行の最初の列を取り出し、スペースで分割して、最初のデータ(日付)を取り出す
        train_start = df.iat[0, 0].split()[0]   
        test_end = df.iat[-1, 0].split()[0]

        # 日付型に変換する
        tdatetime = datetime.strptime(test_end, '%d/%m/%Y')   

        # 一か月前の日付(訓練データの終了日)
        train_end = tdatetime - relativedelta(month=settings.TEST_MONTH)
        # その次の日(テストデータの開始日)
        test_start = train_end + timedelta(days=1)      

        # 日付を文字列にして、スペースで分割して、最初のデータ(日付)を取り出す
        train_end = str(train_end).split()[0]
        test_start = str(test_start).split()[0] 


        # 列名を変更する(cur1 -> 50K, cur2 -> 100K)
        # アップロード時に変更しているためだが、元のアップロードデータを変更するのが良い
        df = df.rename(columns={'cur1': '50K'}, index={'cur2': '100K'})

        # 金種分、学習を実行
        for currency in settings.CURRENCY_LIST:

            # 学習とベストモデルの取得
            best_model_type, best_model_filename, mse_train, mse_test  = bnp_train(
                                                                            settings.MODEL_LIST, 
                                                                            settings.HOLIDAY_LIST, 
                                                                            currency, train_start, 
                                                                            train_end, test_start, 
                                                                            test_end, df)

            # machine_id, currencyですでに登録されているかチェックする
            train_result = db.session.query(Train_result).filter(Train_result.machine_id==machine_id, Train_result.currency == currency).all()

            # 登録済みなら、一旦削除する
            if train_result is not None:
                train_result = db.session.query(Train_result).filter(Train_result.machine_id==machine_id, Train_result.currency == currency).delete()
                db.session.commit()

            # 結果をDBに書き込む
            train_result = Train_result(
                machine_id = machine_id,
                currency = currency,
                train_start = train_start,
                train_end = train_end,
                test_start = test_start,
                test_end = test_end,
                best_model_type = best_model_type,
                mse_train = mse_train,
                mse_test = mse_test,
                best_model_filename = best_model_filename,
            )
            db.session.add(train_result)
            db.session.commit()

            # 学習結果の辞書を作る
            result = {
                "currency": currency,
                "best_model_type": best_model_type,
                "mse_train": mse_train,
                "mse_test" : mse_test,
            }

            # すべての金種の学習結果リストに追加する
            train_resp.append(result)

    print('api_train() : 学習結果\n',train_resp)
    return train_resp
