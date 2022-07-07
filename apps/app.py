from flask import Flask

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# ----------------------------------------------------------------
# インスタンス化する
# ----------------------------------------------------------------
db = SQLAlchemy()           # SQL Alchemy

# ----------------------------------------------------------------
# create_app()を作成する
# ----------------------------------------------------------------

# Flaskインスタンスを作成する
app = Flask(__name__)

# config_keyにマッチする環境のコンフィグクラスを読み込む
app.config.from_object('apps.config')

# ----------------------------------------------------------------
# アプリを連携する
# ----------------------------------------------------------------
db.init_app(app)    # SQLAlchemy
Migrate(app, db)    # Migrate

# ----------------------------------------------------------------
# パッケージからviewsをimport
# ----------------------------------------------------------------
# api
from apps.api import api
app.register_blueprint(api, url_prefix="/api")

from apps.crud import crud
app.register_blueprint(crud, url_prefix="/crud")






