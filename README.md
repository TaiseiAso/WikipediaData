# WikipediaData
***
## 概要
ウィキペディアコーパスから記事部分のみを抽出し形態素解析をするツール。

## 要件
- python3
- yaml
- MeCab
- 必要ファイルをダウンロード
    - WikiExtractor.py
    - jawiki-latest-pages-articles.xml.bz2

## 使い方
1. https://github.com/attardi/wikiextractor から WikiExtractor.py をダウンロードして "script/" に保存。

2. https://dumps.wikimedia.org/jawiki から jawiki-latest-pages-articles.xml.bz2 をダウンロードして "data/" に保存。

3. ウィキペディアコーパスを解凍して記事のみを抽出して一つのファイルにまとめて "data/" に保存。
    ```
    $ python unzip.py
    ```
    保存されるファイル名は、 "config/config.yml" に保存した名前になる。

4. 解凍した記事を形態素解析したウィキペディア記事コーパスを "wakati/" に保存する。
    ```
    $ python wakati.py
    ```

5. 形態素解析したウィキペディア記事コーパスを長さでフィルタリングして、 "filtered/" に保存。
    ```
    $ python filter.py
    ```
    フィルタ処理の内容は、 "config/config.yml" を編集することで変更できる。

6. ウィキペディアコーパスをすべて削除する。
    ```
    $ python clear.py
    ```

## 設定
"config/config.yml" の各値の説明は以下の通り。

- filename: 保存されるファイルの名前
    - wiki_file: ウィキペディアコーパス
- filter: フィルタ処理の内容
    - len_min: 全体の長さの最小
    - len_max: 全体の長さの最大
