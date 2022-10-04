import pandas as pd
import pickle

from apps.crud.models import Cash, Train_result
from apps.app import app
from apps.app import db

#from predictor.api import db
from bnp.interface import bnp_prediction
from bnp.get_rep_notes import get_rep_notes

CURRENCY_NUM = 2    # 金種数        
CASETTE_CAP = 4500  # 金種カセット容量(とりあえず金種で同じとする。)

# カセット装填枚数パターン設定(ex. [[1000, 1000]] 金種毎の配列)
START_NUM = 500     # この枚数から
END_NUM = 4500      # この枚数まで
STEP_NUM = 100      # この枚数刻みで、CASETTE_CAPを超えないカセットパターンを作成する

def api_rep_notes(machine_id, rep_date):

    rep_notes_resp = []
    PRED_DAYS = 30          # 予測する日数

    # 日付型に変換
    from datetime import datetime, timedelta
    rep_date = datetime.strptime(rep_date, '%Y-%m-%d')
    # rep_dateの30日先
    pred_end = rep_date + timedelta(days=PRED_DAYS)

    # 文字列に戻す
    pred_end = pred_end.strftime("%Y-%m-%d")
    rep_date = rep_date.strftime("%Y-%m-%d")
    print('精査日',rep_date)
    print('予測終了日',pred_end)

    currency_list = ['50K', '100K']
    predict_data = []

    for i, currency in enumerate(currency_list):

        # データベースより、machine_id,currencyのモデルを読み込む
        train_result = db.session.query(Train_result).filter(Train_result.machine_id == machine_id, Train_result.currency == currency).first()
        #print(df_train_result)
        if train_result != None:

            # モデルパスの取得
            best_model_filename = train_result.best_model_filename

            # 予測
            df_pred_result = bnp_prediction(rep_date, pred_end, best_model_filename)
            # 需要結果を整数にする
            df_pred_result['demand'] = df_pred_result['demand'].astype('int')

            # リストとして保管
            predict_data.append(df_pred_result['demand'].to_list())

    print('予測データ',predict_data)


    # カセット容量(ex.[2500, 2500] 金種毎の配列)
    cash_full_num = [CASETTE_CAP for i in range(CURRENCY_NUM)]

    # 切れ枚数(ex. [100, 100] 金種毎の配列)
    cash_empty_num =  [100 for i in range(CURRENCY_NUM)]

    rep_notes_result = get_rep_notes(predict_data, cash_empty_num, cash_full_num)
    print('最適な補充枚数', rep_notes_result)

    for i, currency in enumerate(currency_list):

        # JSON形式のレスポンスを作成
        result = {
            "currency": currency,
            "notes": rep_notes_result[i][0],
            "max_days": rep_notes_result[i][1],
            "incident": rep_notes_result[i][2],
        }

        # すべての金種の学習結果
        rep_notes_resp.append(result)

    return rep_notes_resp
