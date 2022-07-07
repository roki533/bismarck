from datetime import datetime

from apps.app import db
#### モデルの定義

# 元データ
class Cash(db.Model):
    # テーブル名を指定する
    __tablename__ = "cash"
    # カラムを定義する
    id = db.Column(db.Integer, db.Sequence('user_id_seq'), primary_key=True)
    machine_id = db.Column(db.String)
    
    date = db.Column(db.String)
    deposit = db.Column(db.Integer)
    withdraw = db.Column(db.Integer)
    cur1 = db.Column(db.Integer)
    cur2 = db.Column(db.Integer)
    a = db.Column(db.Float)
    b = db.Column(db.Float)
    c = db.Column(db.Float)
    d = db.Column(db.Float)
    e = db.Column(db.Float)
    f = db.Column(db.Float)
    r = db.Column(db.Float)

# 学習結果
class Train_result(db.Model):
    # テーブル名を指定する
    __tablename__ = "train_result"
    # カラムを定義する
    id = db.Column(db.Integer, db.Sequence('user_id_seq'), primary_key=True)

    machine_id = db.Column(db.String)
    currency = db.Column(db.String)

    train_start = db.Column(db.String)
    train_end = db.Column(db.String)
    test_start = db.Column(db.String)
    test_end = db.Column(db.String)
    best_model_type = db.Column(db.String)
    mse_train = db.Column(db.Float)
    mse_test = db.Column(db.Float)
    best_model_filename = db.Column(db.String)
    #best_model = db.Column(db.BLOB)

    date = db.Column(db.DateTime, default=datetime.now)