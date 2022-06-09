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
def scraping(url, date, area_name):
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
        data_list.append(area_name)
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
def create_csv(area_id, area_name, area_point):
    # csv出力先ディレクトリ
    output_dir = os.path.dirname(__file__)

    # 出力ファイル名
    output_file = "weather_information_daily_" + area_name + ".csv"

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
                  "prec_no=%d&block_no=%d&year=%d&month=%d&day=&view=" % (int(area_id), int(area_point), date.year, date.month)

            data_per_day = scraping(url, date, area_name)

            for dpd in data_per_day:
                writer.writerow(dpd)

            date = date + relativedelta.relativedelta(months=1)


# ----------------------------------------
# メイン処理
# ----------------------------------------
if __name__ == '__main__':
    area_names = {
        '44': 'Tokyo',
        '62': 'Osaka',
        '51': 'Nagoya'
    }

    point_nums = {
        '44': '47662',
        '62': '47772',
        '51': '47636'
    }

    for area_key in area_names.keys():
        area_id = area_key
        area_name = area_names[area_key]
        area_point = point_nums[area_key]

        create_csv(area_id, area_name, area_point)
