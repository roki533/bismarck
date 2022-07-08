import requests

# MINEタイプ
XLSX_MIMETYPE = 'text/csv'

# <form action="/data/upload" method="post" enctype="multipart/form-data">
#   <input type="file" name="uploadfile"/>
#   <input type="submit" value="submit"/>
# </form>

# main
if __name__ == "__main__":

    # ファイルの準備
    fileName = './986027.csv'
    fileDataBinary = open(fileName, 'rb').read()
    files = {'machine_id': "ws0001", 'uploadfile': (fileName, fileDataBinary, XLSX_MIMETYPE)}

    # ファイルのアップロード
    url = 'http://127.0.0.1:5000/api/upload'
    response = requests.post(url, files=files)

    print(response.status_code)
    print(response.content)