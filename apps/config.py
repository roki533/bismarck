# 環境の設定
from pathlib import Path

# ディレクトリパス
basedir = Path(__file__).parent.parent

# DB
SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir / 'local.sqlite'}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False # 実行SQLのコンソール表示

