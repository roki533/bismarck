import sys

import requests

# MINEタイプ
XLSX_MIMETYPE = 'text/csv'

# <form action="/data/upload" method="post" enctype="multipart/form-data">
#   <input type="file" name="uploadfile"/>
#   <input type="submit" value="submit"/>
# </form>

# main
if __name__ == "__main__":

    args = sys.argv

    if len(args) == 1:
        machine_id = "ws0000"
    else:
        machine_id = args[1]

    # ファイルの準備
    fileName = './986027.csv'
    fileDataBinary = open(fileName, 'rb').read()
    files = {'uploadfile': (fileName, fileDataBinary, XLSX_MIMETYPE)}
    payload = {'machine_id': machine_id}

    # ファイルのアップロード
    url = 'http://127.0.0.1:5000/api/upload'
    response = requests.post(url, data=payload, files=files)

    print(response.status_code)
    print(response.content)