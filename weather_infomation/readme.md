# 気象情報を取得してcsvファイルへ書き出す

## 概要

* 下記サイトで公開されているプログラムの流用
  * https://www.gis-py.com/entry/scraping-weather-data

## 対象URL

* 気象庁サイトから日ごとの値を取得する
  * https://www.data.jma.go.jp/obd/stats/etrn/index.php?prec_no=&block_no=&year=&month=&day=&view=

## 処理内容

1. 気象庁のWebサイトから日ごとの気象情報を取得する
2. 取得結果をcsvファイルに出力する

## csvファイル

* 実行ファイルと同一フォルダに出力する
* ファイルは地域ごとに分ける
* 以下のヘッダを保持する
  * 年月日, 地域, 現地気圧, 海面気圧,
  * 合計降水量, 最大降水量（1時間）, 最大降水量（10分間）, 平均気温, 最高気温, 最低気温,
  * 平均湿度, 最小湿度, 平均風速, 日照時間, 降雪, 最深積雪

## 対象地域

* 以下の辞書型変数に定義した地域が処理対象となる
  * prec_info
    * 都道府県番号と都道府県名
  * block_info
    * 都道府県番号と地点番号

## 対象期間

* __start_date__ で定義した年月日から実行日の前月まで

## 備考

* 対象地域は基本的に各都道府県の庁所在地を設定している
* 庁所在地以外を採用しているもの
  * 東京都
    * 新宿→東京
  * 埼玉県
    * さいたま→熊谷
  * 滋賀県
    * 大津→彦根