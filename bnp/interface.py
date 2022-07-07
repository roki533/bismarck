import pandas as pd
import pickle

from pathlib import Path

def bnp_train(model_list, df_train, df_test):

    print(model_list)
    print(df_train)
    print(df_test)

    best_model_type = "reg_mva14"

    import pickle

    mydata = [{'name': 'shinji kawasaki', 'age': 120, 'height': 230, 'weight': 300},
            {'name': 'isshiki masahiko', 'age': 60, 'height': 180, 'weight': 60}]
    some_data = 100
    another_data = 'deep insider'

    #best_model = open('./bnp/mydata.pickle', 'wb')
    #pickle.dump(mydata, best_model)
    #pickle.dump(some_data, best_model)
    #pickle.dump(another_data, best_model)
    #best_model.close()

    #with open('./bnp/mydata.pickle', 'rb') as f:
    #    best_model = pickle.load(f)
    #    print(best_model)

    best_model_filename = './bnp/W001_50k_reg_mva14.pickle'

    mse_train = 65437.98
    mse_test = 86598.94

    return best_model_type, mse_train, mse_test, best_model_filename





def bnp_prediction(pred_start, pred_end, model):

    print(model)
    print(pred_start, pred_end)

    # テスト用ダミー
    df_pred_result = pd.read_csv("./bnp/reg_mva14_predict_result.csv")

    return df_pred_result
