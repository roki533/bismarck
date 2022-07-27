import pandas as pd
import pickle

from apps.crud.models import Cash, Train_result
from apps.app import app
from apps.app import db

#from predictor.api import db
from bnp.interface import bnp_prediction

def api_predict(machine_id, pred_start, pred_end):

    predict_resp = []

    currency_list = ['50K', '100K']

    for currency in currency_list:

        # データベースより、machine_id,currencyのモデルを読み込む
        train_result = db.session.query(Train_result).filter(Train_result.machine_id == machine_id, Train_result.currency == currency).first()
        #print(df_train_result)
        if train_result != None:

            # モデルパスの取得
            best_model_filename = train_result.best_model_filename

            # 予測
            df_pred_result = bnp_prediction(pred_start, pred_end, best_model_filename)
            # 需要結果を整数にする
            df_pred_result['demand'] = df_pred_result['demand'].astype('int')
            # 結果をリスト形式にする
            pred = df_pred_result.to_numpy().tolist()

            # JSON形式のレスポンスを作成
            result = {
                "currency": currency,
                "predict": pred,
            }

            # すべての金種の学習結果
            predict_resp.append(result)

    return predict_resp
