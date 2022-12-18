# YouTubeのコメント情報をテキストファイルに書き出す

## 対象URLのサンプル

* SOUL'd OUT　『Magenta Magenta』
  * https://www.youtube.com/watch?v=qbEx4fK6TKE
* SOUL'd OUT　『TOKYO通信 ～Urbs Communication～』
  * https://www.youtube.com/watch?v=SO51jyCs3PA

## 処理内容

1. 対象のURLを開く
2. 可能な限りページをスクロールする
3. コメント情報を取得する
4. Good評価が1つ以上あればコメントを取得する
5. 取得したGood数とコメントをテキストファイルに出力する

## 入力ファイル

* ファイル名：url_list.txt
* 実行ディレクトリに配置する

## 出力ファイル

* ファイル名：ページタイトル.txt
* 実行ディレクトリに出力される

## ページスクロールの処理概要

1. スクロール前のコメントエリアのサイズを取得
2. ページのスクロールを実行
3. スクロール後のコメントエリアのサイズを取得
4. スクロール前後のサイズを比較
5. 4.で違いがなくなるまで繰り返し

## 注意

* バックグラウンドで実行しているが音声が流れる