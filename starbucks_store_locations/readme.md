# 処理概要

スターバックスの店舗情報をテキストファイルに書き出す

## 処理内容

1. スターバックスのWebサイトを開く
2. 各都道府県を選択する
3. 検索結果に表示される店舗情報を取得する
4. 取得した情報をテキストファイルに出力する

### 対象URL

* スターバックスのWebサイト
  * https://store.starbucks.co.jp/

### 出力ファイル

* ファイル名：都道府県名.txt
* 実行ディレクトリに出力される
* ファイルは都道府県ごとに出力される

### 対象都道府県

* **todofuken_id** に設定した数値の範囲で指定する
* 北から順に 1:北海道 ～ 47:沖縄 が設定されている
* **range(1, 48)** で全都道府県が対象になる
