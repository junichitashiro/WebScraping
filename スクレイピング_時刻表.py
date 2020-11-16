# ----------------------------------------
# 乗換案内の検索結果をテキストファイルに書き出す
# ----------------------------------------


# ----------------------------------------
# モジュールのインポート
# ----------------------------------------
from selenium import webdriver


# ----------------------------------------
# 変数の設定
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

# ブラウザを起動して最大化する
driver = webdriver.Chrome(cd_path, options=chrome_options)
driver.maximize_window()

# 対象のURLを開く
driver.get('https://www.jorudan.co.jp/norikae/')

# 出発地エリア入力
xpath = '//*[@id="eki1_in"]'
driver.find_element_by_xpath(xpath).send_keys('新宿')
# 到着地エリア入力
xpath = '//*[@id="eki2_in"]'
driver.find_element_by_xpath(xpath).send_keys('東京')
# 検索ボタンクリック
xpath = '//*[@id="search_body"]/div[3]/input'
driver.find_element_by_xpath(xpath).click()

# 経路の要素数を格納する
# 出発時刻が過ぎていても表示されるので0にはならない想定
e_cnt = driver.find_elements_by_class_name('t1')

with open('timetable.txt', 'w') as f:
    # 要素数だけ経路の発着時間のテキストを取得するして書き出す
    for i in range(len(e_cnt)):
        xpath = '//*[@id="Bk_list_tbody"]/tr[' + str(i + 1) + ']/td[2]'
        f.write(driver.find_element_by_xpath(xpath).text + '\n')


# ----------------------------------------
# 処理終了
# ----------------------------------------
print('<<<処理終了')

# ブラウザを閉じる
driver.quit()
