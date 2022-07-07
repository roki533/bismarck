import pandas as pd

# 訓練
def bnp_train(model_list, currency, train_start, train_end, test_start, test_end, df):

    print(model_list, currency, train_start, train_end, test_start, test_end, df)

    # ダミー戻り値
    best_model_type = "reg_mva14"
    best_model_filename = './bnp/W001_50k_reg_mva14.pickle'
    mse_train = 65437.98
    mse_test = 86598.94

    print("出力パラメータ:", best_model_type, best_model_filename, mse_train, mse_test)

    return best_model_type, best_model_filename, mse_train, mse_test


# 予測
def bnp_prediction(pred_start, pred_end, model):

    print("入力パラメータ:", pred_start, pred_end, model)

    # ダミー戻り値
    df_pred_result = pd.read_csv("./bnp/reg_mva14_predict_result.csv")

    print("出力パラメータ:", df_pred_result)
    return df_pred_result
