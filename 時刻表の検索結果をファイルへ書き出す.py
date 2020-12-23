'''
乗換案内の検索結果をテキストファイルに書き出す処理
出発時刻が過ぎていても結果が表示されるので
検索結果が必ずある前提の処理になっている
'''


# ----------------------------------------
# モジュールのインポート
# ----------------------------------------
from selenium import webdriver


# ----------------------------------------
# 変数の設定
# ----------------------------------------
cd_path = 'C:\\ChromeDriver\\chromedriver.exe'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])


# ----------------------------------------
# 処理開始
# ----------------------------------------
print('>>>処理開始')
driver = webdriver.Chrome(cd_path, options=chrome_options)
driver.maximize_window()
driver.implicitly_wait(10)
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
e_cnt = driver.find_elements_by_class_name('t1')

# 出力処理
with open('timetable.txt', 'w', encoding='utf8') as f:
    for i in range(len(e_cnt)):
        xpath = '//*[@id="Bk_list_tbody"]/tr[' + str(i + 1) + ']/td[2]'
        f.write(driver.find_element_by_xpath(xpath).text + '\n')


# ----------------------------------------
# 処理終了
# ----------------------------------------
print('<<<処理終了')
driver.quit()
