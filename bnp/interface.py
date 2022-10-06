import pandas as pd

# 訓練
def bnp_train(model_list, holiday_list, currency, train_start, train_end, test_start, test_end, df):

    print("BNP入力パラメータ:",model_list, holiday_list, currency, train_start, train_end, test_start, test_end, df.head(5))

    # ダミー戻り値
    best_model_type = "reg_mva14"
    best_model_filename = './reg_mva14_evidence_used_object.pickle'
    mse_train = 65437.98
    mse_test = 86598.94

    print("BNP出力パラメータ:", best_model_type, best_model_filename, mse_train, mse_test)

    return best_model_type, best_model_filename, mse_train, mse_test


# 予測
def bnp_prediction(pred_start, pred_end, best_model_filename):

    print("BNP入力パラメータ:", pred_start, pred_end, best_model_filename)

    # ランダムに指定された日付の予測データを作成する。
    # 日付型に変換
    from datetime import datetime, timedelta
    start_date = datetime.strptime(pred_start, '%Y-%m-%d')
    end_date = datetime.strptime(pred_end, '%Y-%m-%d')
    print(start_date, end_date)

    # 開始と終了の間の日数
    days = (end_date - start_date).days + 1
    print(days)
    # 日付のリスト生成
    date_list = [start_date + timedelta(days=i) for i in range(days)]

    import random
    predict = []
    for date in date_list:
        predict.append([date.strftime("%Y-%m-%d"),random.randint(-1000, 1000)])

    df_pred_result = pd.DataFrame(predict, columns=["time", "demand"],)
    print(df_pred_result)

    # ダミー戻り値
    # = pd.read_csv("./bnp/reg_mva14_predict_result.csv")

    print("BNP出力パラメータ:", df_pred_result.head(5))
    return df_pred_result
