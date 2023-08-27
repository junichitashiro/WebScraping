import chromedriver_binary_sync
from selenium import webdriver
from selenium.webdriver.chrome import service as fs
from selenium.webdriver.common.by import By


# ========================================
# 初期処理
# ========================================
# ChromeDriverをダウンロードしてパスを定数に格納する
CHROMEDRIVER = chromedriver_binary_sync.download(download_dir='chromedriver')
chrome_service = fs.Service(executable_path=CHROMEDRIVER)

# オプションの設定
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])


# ========================================
# メイン処理
# ========================================
print('>処理開始')
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
driver.maximize_window()
driver.implicitly_wait(10)
driver.get('https://www.jorudan.co.jp/norikae/')

# 出発地エリア入力
xpath = '//*[@id="eki1_in"]'
driver.find_element(By.XPATH, xpath).send_keys('新宿')
# 到着地エリア入力
xpath = '//*[@id="eki2_in"]'
driver.find_element(By.XPATH, xpath).send_keys('東京')
# 検索ボタンクリック
xpath = '//*[@id="search_body"]/div[3]/input'
driver.find_element(By.XPATH, xpath).click()
e_cnt = len(driver.find_elements(By.CLASS_NAME, 't1'))

# ------------------------------
# 出力処理
# ------------------------------
with open('timetable.txt', mode='w', encoding='utf-8') as f:
    for i in range(1, e_cnt + 1):
        xpath = f'//*[@id="left"]/div[4]/div[2]/table/tbody/tr[{i}]/td[2]'
        f.write(driver.find_element(By.XPATH, xpath).text + '\n')


# ========================================
# 終了処理
# ========================================
print('<処理終了')
driver.quit()
