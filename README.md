# bismarck

## 環境
Python 3.8.8rc1

## インストール方法

- このGit リポジトリから[Code]-[Download ZIP]でソースコードをダウンロードする。
- ZIPファイルを解凍して、適当な場所にコピーする。
- Pythonをインストールする  
最初の画面下部のapp Python ... PATHにはチェックを入れる。Install Nowを選ぶ。

- コマンドプロンプトを管理者権限で起動

- 解凍したファイルのbismarckディレクトリにcdで移動  
- 仮想環境を構築（初回のみ実施）  
py -m venv venv
- 仮想環境を実行  
venv\Scripts\Activate.bat

プロンプトの先頭に(venv)が追加される  
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
  
## 起動、動作確認
http://127.0.0.1:5000/api/ を実行

以下の表示が出ればOK
```
Bismarck
Successed setup.
BIsmarck is Running well!!
Please check the link

wagger Editor(Open API)
```

## 次回以降の起動

- コマンドプロンプトを管理者権限で起動
- bismarckディレクトリにcdで移動
- 仮想環境を実行  
venv\Scripts\Activate.bat
- flaskの実行  
flask run

## Open APIの環境構築
- Swagger Editorをブラウザで起動する
https://editor.swagger.io/
- サンプルのソースコードが左側に表示されていたら、すべて削除してください。
- bismarckディレクトリにあるopenapi.yamlのコードをコピーして、wagger Editorの左に貼り付ける
- 

image.png
- 右にWeb-APIの仕様が表示されている
- Serversからサーバーを選んでテストを実行する
- テストは、Try itボタンから実行できる

