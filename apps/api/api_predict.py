from apps.crud.models import Train_result
from apps.app import db

import apps.api.settings as settings
from bnp.interface import bnp_prediction

def api_predict(machine_id, pred_start, pred_end):
    """
    指定された期間の予測を行う

    Args:
        machine_id (str) : 装置ID
        pred_start (str) : 予測開始日
        pred_end (str) : 予測終了日

    Returns:
        predict_resp (list): 予測結果

        [{
            currency (str) : 金種

            predict (list) : 予測リスト
                [
                    str : 日付
                    int : 予測枚数
                ]
        }]
    Note:
        リクエスト

        'GET' \  
        'http://127.0.0.1:5000/api/models/ws0001/predict' \  
        -H 'accept: application/json' \  
        -H 'start_date: 2021-11-01' \  
        -H 'end_date: 2021-11-10'  

    """

    # 戻り値
    predict_resp = []

    # 金種で
    for currency in settings.CURRENCY_LIST :

        # データベースより、machine_id,currencyのモデルを読み込む
        train_result = db.session.query(Train_result).filter(Train_result.machine_id == machine_id, Train_result.currency == currency).first()
        #print(df_train_result)

        # データがあれば
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

    print('api_predict() : 予測結果\n',predict_resp)
    return predict_resp
