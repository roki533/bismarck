import pandas as pd

from apps.app import app
from apps.app import db

from apps.crud.models import Cash, Train_result


from bnp.interface import bnp_train

def api_train(machine_id, currency, train_start, train_end, test_start, test_end):

    # DBよりモデルタイプ名を読み込む
    #model_list = db.session.query(Setting_model).all()
    model_list = ["reg_mva7", "reg_mva14"]

    # データベースより、ATMIDのデータを読み込む
    SQLALCHEMY_DATABASE_URI = app.config['SQLALCHEMY_DATABASE_URI']

    text = "SELECT * FROM cash WHERE machine_id ='" + machine_id + "'"
    df = pd.read_sql_query(sql = text, con=SQLALCHEMY_DATABASE_URI)
    df.drop(['id', 'machine_id'], axis=1, inplace=True) # idとmachine_idを削除

    # 学習とベストモデルの取得
    best_model_type, best_model_filename, mse_train, mse_test  = bnp_train(model_list, currency, train_start, train_end, test_start, test_end, df)

    # 結果をデータベースに保管する
    # モデルを指定されたディレクトリに保存する。
    # 名前は、[machine_id + currency].pickle
    DIR = 'model'

    # machine_id, currencyですでに登録されているかチェックする

    # 未登録なら

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

    return best_model_type, mse_train, mse_test
