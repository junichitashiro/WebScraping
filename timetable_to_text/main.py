# ----------------------------------------
# モジュールのインポート
# ----------------------------------------
import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.chrome import service as fs
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


# ----------------------------------------
# ChromeDriverの設定
# ----------------------------------------
# ChromeDriverの最適化
CHROMEDRIVER = ChromeDriverManager().install()

# オプションの設定
chrome_service = fs.Service(executable_path=CHROMEDRIVER)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])


# ----------------------------------------
# 処理開始
# ----------------------------------------
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
e_cnt = driver.find_elements(By.CLASS_NAME, 't1')

# 出力処理
with open('timetable.txt', 'w', encoding='utf8') as f:
    for i in range(len(e_cnt)):
        xpath = '//*[@id="left"]/div[4]/div[2]/table/tbody/tr[' + str(i + 1) + ']/td[2]'
        f.write(driver.find_element(By.XPATH, xpath).text + '\n')


# ----------------------------------------
# 処理終了
# ----------------------------------------
print('<処理終了')
driver.quit()
