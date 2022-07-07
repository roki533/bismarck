import pandas as pd
import pickle

from apps.crud.models import Cash, Train_result
from apps.app import app
from apps.app import db

#from predictor.api import db
from bnp.interface import bnp_prediction

def api_predict(machine_id, currency, pred_start, pred_end):

    # データベースより、machine_id,currencyのモデルを読み込む
    df_train_result = db.session.query(Train_result).filter(Train_result.machine_id == machine_id, Train_result.currency == currency).first()
    print(df_train_result)

    # モデルパスの取得
    best_model_filename = df_train_result.best_model_filename
    # 絶対パスにする
    print(best_model_filename)

    #with open('./bnp/reg_mva14_evidence_used_object.pickle', 'rb') as f:
    #    model = pickle.load(f)
    #    print(model)
    model = ""

    df_pred_result = bnp_prediction(pred_start, pred_end, model)

    return df_pred_result
