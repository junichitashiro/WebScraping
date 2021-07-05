'''
スターバックスのWebサイトで都道府県ごとに検索を実行して店舗情報を取得する処理
検索対象都道府県は todofuken_id に入る数値の範囲で指定する
北から順に 1:北海道 8：東京 47:沖縄 が設定されており
range(1, 48)で全都道府県が対象になる
'''


# ----------------------------------------
# モジュールのインポート
# ----------------------------------------
import math
import time
import tkinter.messagebox

import selenium.webdriver


# メッセージボックス用の設定
root = tkinter.Tk()
root.withdraw()


# ----------------------------------------
# ChromeDriverの設定
# ----------------------------------------
cd_path = 'chromedriverの絶対パス'
chrome_options = selenium.webdriver.ChromeOptions()
# この処理はブラウザ表示するとエラー要因が増えるため非表示推奨
chrome_options.add_argument('--headless')
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])


# ----------------------------------------
# 処理開始
# ----------------------------------------
print('>>>処理開始')
driver = selenium.webdriver.Chrome(cd_path, options=chrome_options)
driver.maximize_window()
driver.implicitly_wait(10)
driver.get('https://store.starbucks.co.jp/')

for todofuken_id in range(2, 3):    # ここでは青森のみが対象となる設定
    todofuken_xpath = '//*[@id="search_section"]/div[2]/div[1]/div[2]/ul/li[' + str(todofuken_id) + ']/a'

    # 画面遷移
    todofuken_name = driver.find_element_by_xpath(todofuken_xpath).text
    print(' >>処理対象：' + todofuken_name)
    todofuken_chars = len(todofuken_name)
    driver.find_element_by_xpath(todofuken_xpath).click()
    time.sleep(3)   # 後続処理を安定させるためのウェイト

    # 遷移先での情報取得前処理
    result_xpath = '//*[@id="result_title"]'
    result_text = driver.find_element_by_xpath(result_xpath).text
    result_cnt = int(result_text[13 + todofuken_chars:-3])

    # 「もっと見る」ボタンを押せるだけ押す
    if result_cnt > 10:
        push_cnt = math.ceil((result_cnt - 10) / 10)
        more_xpath = '//*[@id="moreList"]'

        for i in range(push_cnt):
            driver.find_element_by_xpath(more_xpath).click()
            time.sleep(1)

    # 店舗情報の取得と出力処理
    print('  >書込処理開始：' + todofuken_name)
    with open(todofuken_name + '.txt', 'w', encoding='utf8') as f:
        i = 0
        for i in range(result_cnt):
            # 要素が画面外にあるとクリックできないのでスクリプト実行で対応する
            driver.execute_script('arguments[0].click();', driver.find_elements_by_class_name('item')[i])
            time.sleep(0.5)
            output_text = driver.find_elements_by_class_name('item')[i].text
            f.write('--------------------\n')
            f.write(output_text[:-2])
    print('  <書込処理終了：' + todofuken_name)

    driver.get('https://store.starbucks.co.jp/')
    time.sleep(3)


# ----------------------------------------
# 処理終了
# ----------------------------------------
print('<<<処理終了')
tkinter.messagebox.showinfo('処理終了', '処理が終了しました')
driver.quit()
