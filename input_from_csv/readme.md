# 処理概要

CSVファイルの値をWebブラウザで入力する

## 処理内容

1. CSVファイルから値を読み込む
2. 読み込んだ値をWebブラウザに入力する
3. Webブラウザで計算処理を実行する
4. 計算結果をメッセージボックスで表示する

### 対象URL

* 下記サイトのエネルギー必要量計算画面を使用する
  * https://keisan.casio.jp/exec/system/1183427246/

### CSVファイル

* ファイル名：input.csv
* 実行ディレクトリに配置する
* 以下のヘッダを保持する
  * 年齢
  * 性別
  * 身体活動レベル
  * 目標体重

