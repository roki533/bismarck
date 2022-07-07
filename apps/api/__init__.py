from flask import Blueprint, jsonify, request

import pandas as pd
import json

from apps.api.api_train import api_train
from apps.api.api_predict import api_predict
from apps.api.api_upload import api_upload

api = Blueprint("api", __name__)

@api.get("/")
def index():
    return jsonify({"index": "ok"}), 201

#@api.post("/upload")
@api.get("/upload")
def upload():
    print(request)
    machine_id = "Hiro"
    df_cash = pd.DataFrame()

    api_upload(machine_id, df_cash)

    return jsonify({"result": "ok"}), 201


# 学習
@api.post("/train")
def train():
    print(request)

    # パラメータを取り出す
    machine_id  = request.json["machine_id"]
    currency    = request.json["currency"]
    train_start = request.json["train_start"]
    train_end   = request.json["train_end"]
    test_start  = request.json["test_start"]
    test_end    = request.json["test_end"]

    #　学習
    best_model_type, mse_train, mse_test = api_train(machine_id, currency, train_start, train_end, test_start, test_end)

    return jsonify({
                    "best_model_type": best_model_type,
                    "mse_train" : mse_train,
                    "mse_test" : mse_test,
                }), 201

# 予測
@api.post("/predict")
def predict():
    print(request)

    # パラメータを取り出す
    machine_id  = request.json["machine_id"]
    currency    = request.json["currency"]
    pred_start = request.json["pred_start"]
    pred_end   = request.json["pred_end"]

    #print(machine_id, currency, pred_start, pred_end)

    df_pred_result = api_predict(machine_id, currency, pred_start, pred_end)#

    print(df_pred_result.to_json(orient='values'))

    return jsonify(json.loads(df_pred_result.to_json(orient='values'))), 201
    #return jsonify(df_pred_result.to_json()), 201
    #return jsonify(json.loads(df_pred_result.to_json())), 201