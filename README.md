# bismarck

## 環境
Python 3.8.8rc1

## インストール方法

### ソースファイルのダウンロード
- このGit リポジトリから[Code]-[Download ZIP]でソースコードをダウンロードする。
- ZIPファイルを解凍して、適当な場所にコピーする。

### Pythonのインストール
- Pythonをダウンロードする(Python 3.8.8rc1で検証済み)
- Pythonをインストールする
最初の画面下部のapp Python ... PATHにはチェックを入れる。Install Nowを選ぶ。

### 仮想環境の構築と起動
- ２回目以降は、下記の「起動、動作確認」を参照
- コマンドプロンプトを管理者権限で起動
- 解凍したファイルのbismarckディレクトリにcdで移動  

- 仮想環境を構築（初回のみ実施）
```  
py -m venv venv
```
- 仮想環境を実行  
```
venv\Scripts\Activate.bat
```

プロンプトの先頭に(venv)が追加される  

### パッケージのインストール  
```
pip install -r requirements.txt  
```
少し時間がかかる
### DBの構築 (初回もしくは再DB構築時のみ) 
```
flask db init  
```
migrationsディレクトリが作成される  
```
flask db migrate  
```
local.sqliteファイルが作成される  
```
flask db upgrade  
```
sqliteにテーブルが作成される  

### flaskの起動
```  
flask run
```
  
### 起動、動作確認
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
```
venv\Scripts\Activate.bat
```
- flaskの実行  
```
flask run
```

## Open APIの環境構築
- Swagger Editorをブラウザで起動する
https://editor.swagger.io/

- 初回のみ以下の操作をおこなう
- サンプルのソースコードが左側に表示されていたら、すべて削除してください。
- bismarckディレクトリにあるopenapi.yamlのコードをコピーして、wagger Editorの左に貼り付ける

## Open APIの環境構築
- 右にWeb-APIの仕様が表示されている
- Serversからサーバーを選んでテストを実行する
- テストは、Try itボタンから実行できる

