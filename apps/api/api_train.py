import pandas as pd
from dateutil.relativedelta import relativedelta
from datetime import datetime, date, timedelta

from apps.app import app
from apps.app import db

from apps.crud.models import Cash, Train_result


from bnp.interface import bnp_train

def api_train(machine_id):

    train_resp = []

    # DBよりモデルタイプ名を読み込む
    #model_list = db.session.query(Setting_model).all()
    model_list = ["reg_mva7", "reg_mva14"]
    holiday_list = ["2020/1/25","2020/3/22"]

    # データベースより、ATMIDのデータを読み込む
    SQLALCHEMY_DATABASE_URI = app.config['SQLALCHEMY_DATABASE_URI']

    text = "SELECT * FROM cash WHERE machine_id ='" + machine_id + "'"
    df = pd.read_sql_query(sql = text, con=SQLALCHEMY_DATABASE_URI)

    if not df.empty:

        df.drop(['id', 'machine_id'], axis=1, inplace=True) # idとmachine_idを削除

        #print(df.head(3))
        #                      date  deposit  withdraw  cur1  ...      d     e    f    r
        #0      01/01/2021 00:06:05        1         0     0  ...  600.0  10.0  0.0  0.0
        #1      01/01/2021 00:10:14        0         1     4  ...  600.0  10.0  0.0  0.0
        #2      01/01/2021 00:10:48        0         1     1  ...  600.0  10.0  0.0  0.0

        # 訓練とテストデータの日付を取り出す
        # ここは改善が必要

        TEST_MONTH = 1   # テストデータの期間

        # 最初の行の最初の列を取り出し、スペースで分割して、最初のデータ(日付)
        train_start = df.iat[0, 0].split()[0]   
        test_end = df.iat[-1, 0].split()[0]

        tdatetime = datetime.strptime(test_end, '%d/%m/%Y')   # 日付型に変換する

        train_end = tdatetime - relativedelta(month=TEST_MONTH)     # 一か月前の日付
        test_start = train_end + timedelta(days=1)      # その次の日

        # 日付を文字列にして、スペースで分割して、最初のデータ(日付) 
        train_end = str(train_end).split()[0]
        test_start = str(test_start).split()[0] 

        # 列名を変更する(cur1 -> 50K, cur2 -> 100K)
        df = df.rename(columns={'cur1': '50K'}, index={'cur2': '100K'})

        # 金種分、学習を実行
        currency_list = ['50K', '100K']
        for currency in currency_list:

            # 学習とベストモデルの取得
            best_model_type, best_model_filename, mse_train, mse_test  = bnp_train(model_list, holiday_list, currency, train_start, train_end, test_start, test_end, df)

            # machine_id, currencyですでに登録されているかチェックする
            train_result = db.session.query(Train_result).filter(Train_result.machine_id==machine_id, Train_result.currency == currency).all()

            print(train_result)
            #text = "SELECT * FROM train_result WHERE machine_id ='" + machine_id + "' AND currency ='" + currency + "'"
            #df = pd.read_sql_query(sql = text, con=SQLALCHEMY_DATABASE_URI)

            # 登録済みなら削除する
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

            # 学習結果
            result = {
                "currency": currency,
                "best_model_type": best_model_type,
                "mse_train": mse_train,
                "mse_test" : mse_test,
            }

            # すべての金種の学習結果
            train_resp.append(result)

    return train_resp
