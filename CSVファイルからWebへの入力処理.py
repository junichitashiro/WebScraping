# ----------------------------------------
# モジュールのインポート
# ----------------------------------------
from selenium import webdriver
import os
import csv
import tkinter as tk
from tkinter import messagebox

# メッセージボックス用の設定
root = tk.Tk()
root.withdraw()


# ----------------------------------------
# csvファイルの読み込み
# ----------------------------------------
csv_file = 'input.csv'
# ファイルがなかったら処理を終了する
if os.path.exists(csv_file):
    with open(csv_file, 'r', encoding='utf8') as f:
        reader = csv.reader(f)
        line = [row for row in reader]
    # ヘッダしか入力がなかったら処理を終了する
    input_row = len(line)
    print('処理対象件数： ' + str(input_row - 1))

    if input_row < 2:
        messagebox.showwarning('件数チェックエラー', '処理対象データがないため処理を終了します。')
        exit()

else:
    messagebox.showerror('ファイルチェックエラー', '『' + csv_file + '』が存在しないため処理を終了します。')
    exit()


# ----------------------------------------
# ChromeDriverの設定
# ----------------------------------------
# ChromeDriverの絶対パス
cd_path = 'C:\\ChromeDriver\\chromedriver.exe'
# ChromeDriverのオプション
chrome_options = webdriver.ChromeOptions()
# ヘッドレスモードで起動
chrome_options.add_argument('--headless')
# enable-automation：ブラウザ起動時のテスト実行警告を非表示
# enable-logging：DevToolsのログを出力しない
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])


# ----------------------------------------
# 処理開始
# ----------------------------------------
print('>>>処理開始')

# ブラウザを起動する
driver = webdriver.Chrome(cd_path, options=chrome_options)
# ブラウザを最大化
driver.maximize_window()
# 要素が見つかるまで最大10秒待つ設定
driver.implicitly_wait(10)

# 対象のURLを開く
driver.get('https://keisan.casio.jp/exec/system/1183427246/')


# ----------------------------------------
# 入力に使用する画面要素の設定
# ----------------------------------------
age_xpath = '//*[@id="var_age"]'
sx0_xpath = '//*[@id="inparea"]/tbody/tr[2]/td[2]/ul/ol/li[5]/label[1]'
sx1_xpath = '//*[@id="inparea"]/tbody/tr[2]/td[2]/ul/ol/li[5]/label[2]'
alv1_xpath = '//*[@id="inparea"]/tbody/tr[3]/td[2]/ul/ol/li[1]/label[1]'
alv2_xpath = '//*[@id="inparea"]/tbody/tr[3]/td[2]/ul/ol/li[1]/label[2]'
alv3_xpath = '//*[@id="inparea"]/tbody/tr[3]/td[2]/ul/ol/li[1]/label[3]'
kg_xpath = '//*[@id="var_kg"]'
ans0_xpath = '//*[@id="ans0"]'
execute_xpath = '//*[@id="executebtn"]'
clear_xpath = '//*[@id="clearbtn"]'


# ----------------------------------------
# 情報の入力と計算の実行
# ----------------------------------------
for i in range(1, input_row):
    # csvファイルの値を変数に格納する
    age = line[i][0]
    sex = line[i][1]
    act_level = line[i][2]
    weight = line[i][3]

    # 設定値の入力
    driver.find_element_by_xpath(age_xpath).send_keys(age)

    if sex == '男':
        driver.find_element_by_xpath(sx0_xpath).click()
    elif sex == '女':
        driver.find_element_by_xpath(sx1_xpath).click()

    if act_level == '低い':
        driver.find_element_by_xpath(alv1_xpath).click()
    elif act_level == '高い':
        driver.find_element_by_xpath(alv3_xpath).click()
    else:
        driver.find_element_by_xpath(alv2_xpath).click()

    driver.find_element_by_xpath(kg_xpath).send_keys(weight)

    # 計算を実行する
    driver.find_element_by_xpath(execute_xpath).click()

    # ----------------------------------------
    # 計算結果の表示
    # ----------------------------------------
    energy = driver.find_element_by_xpath(ans0_xpath).text
    message = str(i) + '／' + str(input_row - 1) + '件目' + '''
    \n１日に必要なエネルギー量は ''' + energy + ' Kcalです'
    messagebox.showinfo('計算結果', message)

    # 表示後に入力内容をクリアする
    driver.find_element_by_xpath(clear_xpath).click()


# ----------------------------------------
# 処理終了
# ----------------------------------------
print('<<<処理終了')

messagebox.showinfo('処理終了', '処理が終了しました')

# ブラウザを閉じる
driver.quit()
