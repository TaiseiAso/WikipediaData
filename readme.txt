以下のURLからWikiExtractor.pyをダウンロードしてscript/ 下に入れる。
https://github.com/attardi/wikiextractor

data/ 下に jawiki-latest-pages-articles.xml.bz2 を入れて、
$ python unzip.py
を実行し解凍して記事本文のみ抽出する。
https://dumps.wikimedia.org/jawiki/

そのあと、
$ python wakati.py
を実行して分かち書きされたウィキペディア記事コーパスを作成する。
