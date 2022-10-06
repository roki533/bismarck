import os
from flask import Blueprint, jsonify, request

from apps.api.api_train import api_train
from apps.api.api_predict import api_predict
from apps.api.api_upload import api_upload
from apps.api.api_rep_notes import api_rep_notes
from apps.api.api_incident import api_incident

# 環境変数からデータサイズ（単位はByte）を制限する
# limit upload file size : 1MB
# ex) set MAX_JSON_CONTENT_LENGTH=1048576
MAX_JSON_CONTENT_LENGTH = int(os.getenv("MAX_JSON_CONTENT_LENGTH", default="0"))

# アップロードされたファイルの場所
# ex) set UPLOAD_DIR_PATH=C:/tmp/flaskUploadDir
UPLOAD_DIR = os.getenv("UPLOAD_DIR_PATH")

# api
api = Blueprint("api", __name__)

# パラメータの検証は行ってません。

#-------------------------------------------------------------------------------
# 起動テスト用のインデックス
#-------------------------------------------------------------------------------
@api.get("/")
def index():
    return '''
            <h1>Bismarck</h1><p>Successed setup. <BR>
            BIsmarck is Running well!!<BR>
            Please check the link</p>
            <a href='https://editor.swagger.io/'>wagger Editor(Open API)</a>
            '''

#-------------------------------------------------------------------------------
# ファイルのアップロード
#-------------------------------------------------------------------------------
@api.post("/data/<machine_id>")
def upload(machine_id):

    # アップロード(api_upload)
    api_upload(machine_id, request)

    return jsonify({"result": "ok"}), 201

#-------------------------------------------------------------------------------
# 学習
#-------------------------------------------------------------------------------
@api.post("/models/<machine_id>")

def train(machine_id):

    #　学習(api_train)
    train_result = api_train(machine_id)

    if train_result != []:
        return jsonify(train_result), 200
    else:
        return jsonify({"result": "no data"}), 201

#-------------------------------------------------------------------------------
# 予測
#-------------------------------------------------------------------------------
@api.get("/models/<machine_id>/predict")
def predict(machine_id):

    # ヘッダーからパラメータを取り出す
    pred_start = request.headers.get('start_date')
    pred_end = request.headers.get('end_date')

    # 予測
    predict_resp = api_predict(machine_id, pred_start, pred_end)

    if predict_resp != []:
        return jsonify(predict_resp), 201
    else:
        return jsonify({"result": "no data"}), 200


#-------------------------------------------------------------------------------
# 装填枚数
#-------------------------------------------------------------------------------
@api.get("/plan/<machine_id>/rep_notes")
def rep_notes(machine_id):

    # ヘッダーからパラメータを取り出す
    rep_date = request.headers.get('rep_date')

    # 最適装填枚数(api_rep_notes)
    rep_notes_resp = api_rep_notes(machine_id, rep_date)

    if rep_notes_resp != []:
        return jsonify(rep_notes_resp), 201
    else:
        return jsonify({"result": "no data"}), 200

#-------------------------------------------------------------------------------
# インシデント発生
#-------------------------------------------------------------------------------
@api.get("/plan/<machine_id>/incident")
def incident(machine_id):

    # ヘッダーからパラメータを取り出す

    pred_start = request.headers.get('pred_start')
    cash_position = int(request.headers.get('cash_position'))

    # インシデント発生予測(api_incident)
    incident_resp = api_incident(machine_id, cash_position, pred_start)

    if incident_resp != []:
        return jsonify(incident_resp), 201
    else:
        return jsonify({"result": "no data"}), 200

