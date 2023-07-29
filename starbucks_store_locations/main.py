import re
import time
import tkinter.messagebox

import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.chrome import service as fs
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager


# ========================================
# 初期処理
# ========================================
# メッセージボックス用の設定
root = tkinter.Tk()
root.withdraw()

# ChromeDriverの最適化
CHROMEDRIVER = ChromeDriverManager().install()

# オプションの設定
chrome_service = fs.Service(executable_path=CHROMEDRIVER)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')   # 画面非表示推奨
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])


# ========================================
# メイン処理
# ========================================
print('>処理開始')
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
driver.maximize_window()
driver.implicitly_wait(10)
driver.get('https://store.starbucks.co.jp/')

# 画面遷移後に都道府県セレクトボックスの要素を取得
time.sleep(3)
selectbox = driver.find_element(By.ID, 'selectbox')

for todofuken_id in range(1, 2):    # ここでは北海道のみが対象となる設定
    Select(selectbox).select_by_value(str(todofuken_id))
    time.sleep(3)

    # 都道府県選択後の情報取得前処理
    todofuken_id += 1
    target = driver.find_element(By.XPATH, f'//*[@id="selectbox"]/option[{todofuken_id}]').text
    print('>>処理対象：' + target)

    todofuken_name = re.sub('( \(+[0-9]+\))', '', target)
    result_text = driver.find_element(By.XPATH, '//*[@id="vue-search"]/div[3]/div[1]/div/div[2]/div[1]/div[3]/div[1]').text
    result_cnt = int(result_text.replace('件', ''))

    # 「もっと見る」ボタンを押せるだけ押しておく
    more_xpath = '//*[@id="vue-search"]/div[3]/div[1]/div/div[2]/div[1]/div[3]/div[2]/div[2]/button'
    try:
        more_button_cnt = len(driver.find_elements(By.XPATH, more_xpath))
    except:
        more_button_cnt = 0

    while more_button_cnt > 0:
        driver.find_element(By.XPATH, more_xpath).click()
        time.sleep(1)
        try:
            more_button_cnt = len(driver.find_elements(By.XPATH, more_xpath))
        except:
            more_button_cnt = 0

    # ------------------------------
    # 店舗情報の取得と出力処理
    # ------------------------------
    print('>>>書込処理開始')
    with open(todofuken_name + '.txt', mode='w', encoding='utf-8') as f:
        i = 1
        for i in range(1, result_cnt + 1):
            output_text = driver.find_element(By.XPATH, f'//*[@id="store-list"]/li[{i}]/div').text
            f.write(f'<{i}>\n')
            f.write(output_text + '\n')
    print('<<<書込処理終了')

    time.sleep(1)


# ========================================
# 終了処理
# ========================================
print('<処理終了')
tkinter.messagebox.showinfo('処理終了', '処理が終了しました')
driver.quit()
