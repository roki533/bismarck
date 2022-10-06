from apps.crud.models import Train_result
from apps.app import db

import apps.api.settings as settings
from bnp.interface import bnp_prediction
from bnp.rep_plan import get_rep_notes


def api_rep_notes(machine_id, rep_date):
    """
    最適な装填枚数を取得する

    Args:
        machine_id (str): 装置ID
        rep_date(str) : 装填する日

    Returns:
        rep_notes_resp : 装填情報リスト
            [{
                currency (str) : 金種
                notes (int): 装填枚数
                max_days (int) : インシデントまでの日数
                incident (int) : インシデント(0:発生なし、1:切れ　2:あふれ)
            }]

    Note:
        リクエスト

    'GET' \
    'http://127.0.0.1:5000/api/plan/ws0001/rep_notes' \
    -H 'accept: application/json' \
    -H 'rep_date: 2021-11-01'

    """
    # レスポンス
    rep_notes_resp = []

    # 日付型に変換
    from datetime import datetime, timedelta
    rep_date = datetime.strptime(rep_date, '%Y-%m-%d')
    # rep_dateの30日先
    pred_end = rep_date + timedelta(days=settings.PRED_DAYS)

    # 文字列に戻す
    pred_end = pred_end.strftime("%Y-%m-%d")
    rep_date = rep_date.strftime("%Y-%m-%d")
    print('精査日',rep_date)
    print('予測終了日',pred_end)

    # 予測結果のリスト
    predict_data = []

    # 予測結果を取得する
    for i, currency in enumerate(settings.CURRENCY_LIST):

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

    # 最適装填枚数を取得する
    rep_notes_result = get_rep_notes(predict_data, settings.CASH_EMPTY_NUM, settings.CASH_FULL_NUM)
    print('最適な補充枚数', rep_notes_result)

    # レスポンスの作成
    for i, currency in enumerate(settings.CURRENCY_LIST):

        # JSON形式のレスポンスを作成
        result = {
            "currency": currency,
            "notes": rep_notes_result[i][0],
            "max_days": rep_notes_result[i][1],
            "incident": rep_notes_result[i][2],
        }

        # すべての金種の学習結果
        rep_notes_resp.append(result)

    print('api_rep_notes() : 装填情報\n',rep_notes_resp)
    return rep_notes_resp
