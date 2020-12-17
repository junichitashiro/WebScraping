# ----------------------------------------
# モジュールのインポート
# ----------------------------------------
from selenium import webdriver
import time
import math
import tkinter as tk
from tkinter import messagebox

# メッセージボックス用の設定
root = tk.Tk()
root.withdraw()


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
driver.get('https://store.starbucks.co.jp/')

# ----------------------------------------
# 処理に使用する画面要素の設定
# ----------------------------------------
more_xpath = '//*[@id="moreList"]'

# 都道府県用のカウンタ 1:北海道 8：東京 47:沖縄
todofuken_cnt = 1
for todofuken_cnt in range(1, 4):
    # 各都道府県画面へのリンクを格納する
    todofuken_xpath = '//*[@id="search_section"]/div[2]/div[1]/div[2]/ul/li[' + str(todofuken_cnt) + ']/a'

    # ----------------------------------------
    # 画面遷移
    # ----------------------------------------
    # 都道府県名の格納
    todofuken_name = driver.find_element_by_xpath(todofuken_xpath).text
    print(' >>処理対象：' + todofuken_name)
    # 対象件数の抽出に使用するため都道府県名の文字数を格納する
    todofuken_len = len(todofuken_name)
    # 各都道府県での検索結果ページへ遷移する
    driver.find_element_by_xpath(todofuken_xpath).click()
    # 件数取得を安定させるためのウェイト
    time.sleep(3)

    # ----------------------------------------
    # 遷移先での情報取得前処理
    # ----------------------------------------
    # ページ上部に表示されている検索結果から件数のみを抽出する
    result_xpath = '//*[@id="result_title"]'
    result_text = driver.find_element_by_xpath(result_xpath).text
    result_cnt = int(result_text[13 + todofuken_len:-3])

    # 「もっと見る」ボタンを押せるだけ押す
    if result_cnt > 10:
        push_cnt = math.ceil((result_cnt - 10) / 10)

        i = 0
        for i in range(push_cnt):
            driver.find_element_by_xpath(more_xpath).click()
            time.sleep(1)

    # ----------------------------------------
    # 店舗情報の取得と出力処理
    # ----------------------------------------
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

    # 都道府県選択画面に戻る
    driver.get('https://store.starbucks.co.jp/')
    time.sleep(3)


# ----------------------------------------
# 処理終了
# ----------------------------------------
print('<<<処理終了')

messagebox.showinfo('処理終了', '処理が終了しました')

# ブラウザを閉じる
driver.quit()
