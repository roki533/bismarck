'''
このファイルは、api以下で利用する設定を集めている
最終的には、DBにて管理し、変更が容易にできるのがよい。
'''

CURRENCY_NUM = 2    # 金種数        
CASETTE_CAP = 4500  # 金種カセット容量(とりあえず金種で同じとする。)

# カセット装填枚数パターン設定(ex. [[1000, 1000]] 金種毎の配列)
START_NUM = 500     # この枚数から
END_NUM = 4500      # この枚数まで
STEP_NUM = 100      # この枚数刻みで、CASETTE_CAPを超えないカセットパターンを作成する

# 最適装填枚数を取得する時に、現金を最小にするための再調整をする
RE_ADJUST = True   

# -- 自動計算 --
# 個別に設定するときは、変更してください。

# カセット容量(ex.[2500, 2500] 金種毎の配列)
CASH_FULL_NUM = [CASETTE_CAP for i in range(CURRENCY_NUM)]

# 切れ枚数(ex. [100, 100] 金種毎の配列)
EMPTY_NUM = 100
CASH_EMPTY_NUM =  [EMPTY_NUM for i in range(CURRENCY_NUM)]

# 容量オーバーチェック
if END_NUM > CASETTE_CAP:
    END_NUM = CASETTE_CAP

if START_NUM < 0:
    START_NUM = 0

CST_PATERN = [[i for i in range(START_NUM, END_NUM+STEP_NUM + 1, STEP_NUM)] for j in range(CURRENCY_NUM)]
#print(CST_PATERN)
# [[500, 600, 700, 800, 900, 1000, 1100,...]]

# -- 自動計算ここまで --


# 学習のテストデータの期間
TEST_MONTH = 1   

# 金種リスト
CURRENCY_LIST = ['50K', '100K']

# モデルリスト
MODEL_LIST = ["reg_mva7", "reg_mva14"]

# 休日リスト
HOLIDAY_LIST = ["2020/1/25","2020/3/22"]

# 最適装填枚数を得るために予測する日数
PRED_DAYS = 30          # 予測する日数