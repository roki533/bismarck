# bismarck

環境
Python 3.8.8rc1

インストール方法

- PowerShellを管理者権限で起動
- PowerShell Set-ExecutionPolicy RemoteSigned CurrentUser を実行
- bismarckディレクトリに移動
- 仮想環境を構築
　py -m venv venv
- 仮想環境を実行
  venv\Scripts\Activate.ps1
- パッケージのインストール
　pip install -r requirements.txx
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
  http://127.0.0.1:5000/api/upload
  
- train
POST : http://127.0.0.1:5000/api/train
{
  "machine_id":"Hiro",
  "currency":"50K", 
  "train_start":"01/01/2021", 
  "train_end":"10/31/2021",
  "test_start":"11/01/2021", 
  "test_end":"11/30/2021"
}

- predict
POST : http://127.0.0.1:5000/api/predict
{
  "machine_id":"Hiro",
  "currency":"50K", 
  "pred_start":"12/01/2021", 
  "pred_end":"12/31/2021"
}
