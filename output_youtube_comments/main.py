# ========================================
# 初期処理
# ========================================
import os
import time
import tkinter.messagebox

import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.chrome import service as fs
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# メッセージボックス用の設定
root = tkinter.Tk()
root.withdraw()

# 入力ファイルの読み込み
input_file = r'url_list.txt'
url_list = []
if os.path.exists(input_file):
    with open(input_file, mode='r', encoding='utf-8') as f:
        for i in f:
            url_list.append(i)

    input_row = len(url_list)
    print(f'処理対象件数： {input_row}')

    if input_row < 1:
        tkinter.messagebox.showwarning('件数チェックエラー', '処理対象データがないため処理を終了します。')
        exit()

else:
    tkinter.messagebox.showerror('ファイルチェックエラー', f'『{input_file}』が存在しないため処理を終了します。')
    exit()

# ChromeDriverの最適化
CHROMEDRIVER = ChromeDriverManager().install()

# オプションの設定
chrome_service = fs.Service(executable_path=CHROMEDRIVER)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])


# ========================================
# メイン処理
# ========================================
print('>処理開始')
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
driver.maximize_window()
driver.implicitly_wait(5)

# リスト中のURLを繰り返す
for url in url_list:
    driver.get(url)
    content = driver.find_element(By.TAG_NAME, 'body')

    # タイトルが取得できなかったらYouTubeページではないと判断
    try:
        title = driver.find_element(By.XPATH, '//*[@id="title"]/h1/yt-formatted-string').text
        print(f'>>ページタイトル：{title}')

        # 事前にページをスクロールしきっておく
        com_area = driver.find_element(By.ID, 'contents')
        before_scroll = com_area.location
        while True:
            print('>>ページスクロール中…')
            content.send_keys(Keys.END)
            time.sleep(3)
            after_scroll = com_area.location
            if before_scroll != after_scroll:
                before_scroll = after_scroll
            else:
                print('<<ページスクロール終了')
                break

        # Good評価のついているコメントを取得して出力する
        print('>>>書込処理開始')
        with open(f'{title}.txt', 'w', encoding='utf8') as f:
            i = 1
            while i > 0:
                try:
                    good_xpath = f'/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-comments/ytd-item-section-renderer/div[3]/ytd-comment-thread-renderer[{i}]/ytd-comment-renderer/div[3]/div[2]/ytd-comment-action-buttons-renderer/div[1]/span[2]'
                    good = driver.find_element(By.XPATH, good_xpath)

                    # Goodが1つ以上あったらその数とコメントを書き込む
                    if good.text != '':
                        com_xpath = f'/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-comments/ytd-item-section-renderer/div[3]/ytd-comment-thread-renderer[{i}]/ytd-comment-renderer/div[3]/div[2]/div[2]/ytd-expander/div/yt-formatted-string'
                        com = driver.find_element(By.XPATH, com_xpath)
                        com_text = com.text.replace('\n', '')
                        f.write(f'【{good.text}】\t')
                        f.write(f'{com_text}\n')

                    i += 1
                except:
                    i = 0
        print('<<<書込処理終了')

    except:
        print('適切なURLではありません')
        pass

    time.sleep(3)


# ========================================
# 終了処理
# ========================================
print('<処理終了')
tkinter.messagebox.showinfo('処理終了', '処理が終了しました')
driver.quit()
