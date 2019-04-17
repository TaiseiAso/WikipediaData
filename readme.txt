data/ 下に jawiki-latest-pages-articles.xml.bz2 を入れて、
$ python unzip.py
を実行し解凍して記事本文のみ抽出する。

そのあと、
$ python wakati.py
を実行して分かち書きされたウィキペディア記事コーパスを作成する。
