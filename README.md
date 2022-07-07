# bismarck

## 環境
Python 3.8.8rc1

## インストール方法

- このGit リポジトリから[Code]-[Download ZIP]でソースコードをダウンロードする。
- ZIPファイルを解凍して、適当な場所にコピーする。
- Pythonをインストールする
　最初の画面下部のapp Python ... PATHにはチェックを入れる。Install Nowを選ぶ。
- PowerShellを管理者権限で起動
- PowerShell Set-ExecutionPolicy RemoteSigned CurrentUser を実行
- 回答したファイルのbismarckディレクトリにcdで移動
- 仮想環境を構築
　py -m venv venv を実行して、Pythonの仮想環境を作る
- 仮想環境を実行
  venv\Scripts\Activate.ps1　を実行する
  プロンプトの先頭に(venv) PS が追加される
- パッケージのインストール
　pip install -r requirements.txt
  少し時間がかかる
- DBの構築
  flask db init
  migrationsディレクトリが作成される
  flask db migrate
  local.sqliteファイルが作成される
  flask db upgrade
  sqliteにテーブルが作成される

- flaskの実行
  flask run
  
- 起動確認
  http://127.0.0.1:5000/api/ を実行

API実行
- Talend API Tester - Free Editionをchromeにインストール
　https://chrome.google.com/webstore/detail/talend-api-tester-free-ed/aejoelaoggembcahagimdiliamlcdmfm?hl=ja

- upload
METHOD : GET
SCHEME : http://127.0.0.1:5000/api/upload
  
- train
METHOD : POST
SCHEME : http://127.0.0.1:5000/api/train
BODY   :
{
  "machine_id":"Hiro",
  "currency":"50K", 
  "train_start":"01/01/2021", 
  "train_end":"10/31/2021",
  "test_start":"11/01/2021", 
  "test_end":"11/30/2021"
}

- predict
METHOD : POST
SCHEME : http://127.0.0.1:5000/api/predict
BODY   :
{
  "machine_id":"Hiro",
  "currency":"50K", 
  "pred_start":"12/01/2021", 
  "pred_end":"12/31/2021"
}
