# ----------------------------------------
# モジュールのインポート
# ----------------------------------------
import csv
import datetime
import os
import urllib.request

from dateutil import relativedelta
from ym import ym
from bs4 import BeautifulSoup


def str2float(weather_data):
    try:
        return float(weather_data)
    except Exception:
        return 0


# ----------------------------------------
# 気象データ取得処理
# ----------------------------------------
def scraping(url, date, prec_name):
    # 気象データのページを取得
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html)
    trs = soup.find("table", {"class": "data2_s"})

    data_list = []
    data_list_per_day = []

    # table の中身を取得
    for tr in trs.findAll('tr')[4:]:
        tds = tr.findAll('td')

        if tds[1].string is None:
            break

        ymd = datetime.datetime(date.year, date.month, int(tds[0].string))
        data_list.append(ymd.strftime('%Y-%m-%d'))
        data_list.append(prec_name)
        data_list.append(str2float(tds[1].string))
        data_list.append(str2float(tds[2].string))
        data_list.append(str2float(tds[3].string))
        data_list.append(str2float(tds[4].string))
        data_list.append(str2float(tds[5].string))
        data_list.append(str2float(tds[6].string))
        data_list.append(str2float(tds[7].string))
        data_list.append(str2float(tds[8].string))
        data_list.append(str2float(tds[9].string))
        data_list.append(str2float(tds[10].string))
        data_list.append(str2float(tds[11].string))
        data_list.append(str2float(tds[16].string))
        data_list.append(str2float(tds[17].string))
        data_list.append(str2float(tds[18].string))

        data_list_per_day.append(data_list)

        data_list = []

    return data_list_per_day


# ----------------------------------------
# csv出力処理
# ----------------------------------------
def create_csv(prec_no, prec_name, block_no):
    # csv出力先ディレクトリ
    output_dir = os.path.dirname(__file__)

    # 出力ファイル名
    output_file = "weather_information_daily_" + prec_name + ".csv"

    # データ取得開始日
    start_date = datetime.date(2020, 1, 1)

    # データ取得終了日 = 実行日
    end_date = datetime.date.today()

    # csvヘッダ
    fields = ["年月日", "地域", "現地気圧", "海面気圧", "合計降水量", "最大降水量（1時間）", "最大降水量（10分間）",
              "平均気温", "最高気温", "最低気温", "平均湿度", "最小湿度", "平均風速", "日照時間", "降雪", "最深積雪"]

    with open(os.path.join(output_dir, output_file), 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(fields)

        # 実行日前月までを取得対象期間とする
        date = start_date
        while ym(date.year, date.month) != ym(end_date.year, end_date.month):

            # 対象url
            url = "http://www.data.jma.go.jp/obd/stats/etrn/view/daily_s1.php?" \
                  "prec_no=%d&block_no=%d&year=%d&month=%d&day=&view=" % (int(prec_no), int(block_no), date.year, date.month)

            data_per_day = scraping(url, date, prec_name)

            for dpd in data_per_day:
                writer.writerow(dpd)

            date = date + relativedelta.relativedelta(months=1)


# ----------------------------------------
# メイン処理
# ----------------------------------------
if __name__ == '__main__':
    prec_info = {
        '14': '北海道'
        , '31': '青森県'
        , '33': '岩手県'
        , '34': '宮城県'
        , '32': '秋田県'
        , '35': '山形県'
        , '36': '福島県'
        , '40': '茨城県'
        , '41': '栃木県'
        , '42': '群馬県'
        , '43': '埼玉県'
        , '45': '千葉県'
        , '44': '東京都'
        , '46': '神奈川県'
        , '54': '新潟県'
        , '55': '富山県'
        , '56': '石川県'
        , '57': '福井県'
        , '49': '山梨県'
        , '48': '長野県'
        , '52': '岐阜県'
        , '50': '静岡県'
        , '51': '愛知県'
        , '53': '三重県'
        , '60': '滋賀県'
        , '61': '京都府'
        , '62': '大阪府'
        , '63': '兵庫県'
        , '64': '奈良県'
        , '65': '和歌山県'
        , '69': '鳥取県'
        , '68': '島根県'
        , '66': '岡山県'
        , '67': '広島県'
        , '81': '山口県'
        , '71': '徳島県'
        , '72': '香川県'
        , '73': '愛媛県'
        , '74': '高知県'
        , '82': '福岡県'
        , '85': '佐賀県'
        , '84': '長崎県'
        , '86': '熊本県'
        , '83': '大分県'
        , '87': '宮崎県'
        , '88': '鹿児島県'
        , '91': '沖縄県'
    }

    block_info = {
        '14': '47412'
        , '31': '47575'
        , '33': '47584'
        , '34': '47590'
        , '32': '47582'
        , '35': '47588'
        , '36': '47595'
        , '40': '47629'
        , '41': '47615'
        , '42': '47624'
        , '43': '47626'
        , '45': '47682'
        , '44': '47662'
        , '46': '47670'
        , '54': '47604'
        , '55': '47607'
        , '56': '47605'
        , '57': '47616'
        , '49': '47638'
        , '48': '47610'
        , '52': '47632'
        , '50': '47656'
        , '51': '47636'
        , '53': '47651'
        , '60': '47761'
        , '61': '47759'
        , '62': '47772'
        , '63': '47770'
        , '64': '47780'
        , '65': '47777'
        , '69': '47746'
        , '68': '47741'
        , '66': '47768'
        , '67': '47765'
        , '81': '47784'
        , '71': '47895'
        , '72': '47891'
        , '73': '47887'
        , '74': '47893'
        , '82': '47807'
        , '85': '47813'
        , '84': '47817'
        , '86': '47819'
        , '83': '47815'
        , '87': '47830'
        , '88': '47827'
        , '91': '47936'
    }

    for prec_no in prec_info.keys():
        prec_name = prec_info[prec_no]
        block_no = block_info[prec_no]

        create_csv(prec_no, prec_name, block_no)
