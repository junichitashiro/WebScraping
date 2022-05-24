'''
csvファイルの値をWebサイト上で連続入力する処理
'''


# ----------------------------------------
# モジュールのインポート
# ----------------------------------------
import csv
import os
import tkinter.messagebox

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs


# メッセージボックス用の設定
root = tkinter.Tk()
root.withdraw()


# ----------------------------------------
# csvファイルの読み込み
# ----------------------------------------
csv_file = 'input.csv'
if os.path.exists(csv_file):
    with open(csv_file, 'r', encoding='utf8') as f:
        reader = csv.reader(f)
        line = [row for row in reader]

    input_row = len(line)
    print('処理対象件数： ' + str(input_row - 1))

    if input_row < 2:
        tkinter.messagebox.showwarning('件数チェックエラー', '処理対象データがないため処理を終了します。')
        exit()

else:
    tkinter.messagebox.showerror('ファイルチェックエラー', '『' + csv_file + '』が存在しないため処理を終了します。')
    exit()


# ----------------------------------------
# ChromeDriverの設定
# ----------------------------------------
CHROMEDRIVER = r'C:\chromedriver\chromedriver.exe'
chrome_service = fs.Service(executable_path=CHROMEDRIVER)
chrome_options = webdriver.ChromeOptions()
# ブラウザ表示が不要な場合はコメントインする
# chrome_options.add_argument('--headless')
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])


# ----------------------------------------
# 処理開始
# ----------------------------------------
print('>>>処理開始')
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

driver.maximize_window()
driver.implicitly_wait(10)
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
    age = line[i][0]
    sex = line[i][1]
    act_level = line[i][2]
    weight = line[i][3]

    driver.find_element(By.XPATH, age_xpath).send_keys(age)

    if sex == '男':
        driver.find_element(By.XPATH, sx0_xpath).click()
    elif sex == '女':
        driver.find_element(By.XPATH, sx1_xpath).click()

    if act_level == '低い':
        driver.find_element(By.XPATH, alv1_xpath).click()
    elif act_level == '高い':
        driver.find_element(By.XPATH, alv3_xpath).click()
    else:
        driver.find_element(By.XPATH, alv2_xpath).click()

    driver.find_element(By.XPATH, kg_xpath).send_keys(weight)

    driver.find_element(By.XPATH, execute_xpath).click()

    # 計算結果の表示
    energy = driver.find_element(By.XPATH, ans0_xpath).text
    message = str(i) + '／' + str(input_row - 1) + '件目' + '''
    \n１日に必要なエネルギー量は ''' + energy + ' Kcalです'
    tkinter.messagebox.showinfo('計算結果', message)
    driver.find_element(By.XPATH, clear_xpath).click()


# ----------------------------------------
# 処理終了
# ----------------------------------------
print('<<<処理終了')
tkinter.messagebox.showinfo('処理終了', '処理が終了しました')
driver.quit()
