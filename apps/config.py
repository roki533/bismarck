from pathlib import Path

basedir = Path(__file__).parent.parent

SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir / 'local.sqlite'}"
SQLALCHEMY_TRACK_MODIFICATIONS = False

SQLALCHEMY_ECHO = False # 実行SQLのコンソール表示

