from apps.crud.models import Cash, Train_result
from apps.app import db

import apps.api.settings as settings
from bnp.interface import bnp_prediction
from bnp.rep_plan import get_incident_days

def api_incident(machine_id, cash_position, pred_start):
    """
    発生インシデント(切れ/あふれ)までの日数を取得する

    Args:
        machine_id (str): 装置ID
        cash_position(int) : 予測を開始する日の現金の残量
        pred_start(str) : 予測を開始する日

    Returns:
        rep_notes_resp : 装填情報リスト
            [{
                currency (str) : 金種
                max_days (int) : インシデントまでの日数
                incident (int) : インシデント(0:発生なし、1:切れ　2:あふれ)
            }]

    Note:
        リクエスト例

        'GET' \
        'http://127.0.0.1:5000/api/plan/ws0001/incident' \
        -H 'accept: application/json' \
        -H 'pred_start: 2021-11-01' \
        -H 'cash_position: 2000'

    """

    incident_resp = []
    PRED_DAYS = 30          # 予測する日数

    # 日付型に変換
    from datetime import datetime, timedelta
    pred_start = datetime.strptime(pred_start, '%Y-%m-%d')
    # rep_dateの30日先
    pred_end = pred_start + timedelta(days=PRED_DAYS)

    # 文字列に戻す
    pred_end = pred_end.strftime("%Y-%m-%d")
    pred_start = pred_start.strftime("%Y-%m-%d")

    currency_list = ['50K', '100K']
    predict_data = []

    # 金種
    for i, currency in enumerate(currency_list):

        # データベースより、machine_id,currencyのモデルを読み込む
        train_result = db.session.query(Train_result).filter(Train_result.machine_id == machine_id, Train_result.currency == currency).first()
        # 予測データがあれば
        if train_result != None:

            # モデルパスの取得
            best_model_filename = train_result.best_model_filename

            # 予測
            df_pred_result = bnp_prediction(pred_start, pred_end, best_model_filename)
            # 需要結果を整数にする
            df_pred_result['demand'] = df_pred_result['demand'].astype('int')
            # リストにする
            predicts = df_pred_result['demand'].to_list()

            # 金種により、最長の経過日数をシミュレーションで求める
            incident, max_days = get_incident_days(cash_position, predicts, settings.CASH_EMPTY_NUM[i], settings.CASH_FULL_NUM[i])

            # JSON形式のレスポンスを作成
            result = {
                "currency": currency,
                "max_days": max_days,
                "incident": incident,
            }

            # すべての金種の学習結果
            incident_resp.append(result)

    print('api_incident() : インシデント予測結果\n',incident_resp)
    return incident_resp
