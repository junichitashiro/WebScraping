import datetime
import glob

import win32com.client

# ========================================
# 初期処理
# ========================================
# 変数の設定
file_ymd = datetime.datetime.today().strftime('%Y%m%d')
folder_path = r'C:\temp'
file_name = r'\売上報告*_' + file_ymd + '.xlsx'

# Outlookオブジェクトの設定
outlook = win32com.client.Dispatch('Outlook.Application')
mail = outlook.CreateItem(0)

# メール内容の設定
mail.bodyformat = 1  # 1:テキスト 2:HTML 3:リッチテキスト
mail.to = 'tokyo@test.com ; nagoya@test.com ; osaka@test.com'
mail.subject = '日時売上報告' + file_ymd
mail.body = '''\
売上報告書を送信します。
'''

# 添付ファイルの設定
# ワイルドカードで添付ファイルを指定する
files = glob.glob(folder_path + file_name)
print('---添付ファイルを表示---')
for add_file in files:
    print(glob.glob(add_file))
    mail.attachments.Add(add_file)

# ========================================
# メイン処理
# ========================================
if len(files) == 0:
    print('---添付ファイルがありません---')

elif len(files) != 3:
    mail.body = mail.body + '\n※添付ファイルに過不足があります'
    mail.display(True)
    # mail.Send()
    print('---メール送信完了---')

else:
    mail.display(True)
    # mail.Send()
    print('---メール送信完了---')
