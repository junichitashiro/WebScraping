# ----------------------------------------
# モジュールのインポート
# ----------------------------------------
import re
import time
import tkinter.messagebox

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs
from selenium.webdriver.support.select import Select


# メッセージボックス用の設定
root = tkinter.Tk()
root.withdraw()


# ----------------------------------------
# ChromeDriverの設定
# ----------------------------------------
CHROMEDRIVER = r'C:\chromedriver\chromedriver.exe'
chrome_service = fs.Service(executable_path=CHROMEDRIVER)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])


# ----------------------------------------
# 処理開始
# ----------------------------------------
print('>処理開始')
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
driver.maximize_window()
driver.implicitly_wait(10)
driver.get('https://store.starbucks.co.jp/')

# 画面遷移後に都道府県セレクトボックスの要素を取得
time.sleep(3)
selectbox = driver.find_element(By.ID, 'selectbox')

for todofuken_id in range(2, 3):    # ここでは青森のみが対象となる設定
    Select(selectbox).select_by_value(str(todofuken_id))
    time.sleep(3)

    # 都道府県選択後の情報取得前処理
    todofuken_target = driver.find_element(By.XPATH, '//*[@id="selectbox"]/option[' + str(todofuken_id + 1) + ']').text
    print('>>処理対象：' + todofuken_target)

    todofuken_name = re.sub('( \(+[0-9]+\))', '', todofuken_target)
    result_text = driver.find_element(By.XPATH, '//*[@id="vue-search"]/div[3]/div[1]/div/div[2]/div[1]/div[3]/div[1]').text
    result_cnt = int(result_text.replace('件', ''))

    # 「もっと見る」ボタンを押せるだけ押しておく
    more_xpath = '//*[@id="vue-search"]/div[3]/div[1]/div/div[2]/div[1]/div[3]/div[2]/div[2]/button'
    try :
        more_button_cnt = len(driver.find_elements(By.XPATH, more_xpath))
    except:
        more_button_cnt = 0

    while more_button_cnt > 0:
        driver.find_element(By.XPATH, more_xpath).click
        time.sleep(1)
        try :
            more_button_cnt = len(driver.find_elements(By.XPATH, more_xpath))
        except:
            more_button_cnt = 0


    # 店舗情報の取得と出力処理
    print('>>>書込処理開始')
    with open(todofuken_name + '.txt', 'w', encoding='utf8') as f:
        i = 1
        for i in range(1, result_cnt + 1):
            # 100件ごとに画面を更新する
            if  i % 100 == 0:
                driver.find_element(By.XPATH, '//*[@id="store-list"]/li[' + str(i) + ']/div').click()
                time.sleep(1)

            output_text = driver.find_element(By.XPATH, '//*[@id="store-list"]/li[' + str(i) + ']/div').text
            f.write('<' + str(i) + '>\n')
            f.write(output_text + '\n')
    print('<<<書込処理終了')

    time.sleep(1)


# ----------------------------------------
# 処理終了
# ----------------------------------------
print('<処理終了')
tkinter.messagebox.showinfo('処理終了', '処理が終了しました')
driver.quit()