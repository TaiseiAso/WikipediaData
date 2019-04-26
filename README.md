# WikipediaData
***
## 概要
日本語のウィキペディアコーパスから記事部分のみを抽出し形態素解析をするツール。

## 要件
- Linuxコマンドが使用可能な環境
- python3
- pyyaml
- MeCab
- 必要ファイルをダウンロード
    - WikiExtractor.py
    - jawiki-latest-pages-articles.xml.bz2

## 使い方
1. "script/" フォルダと "data/" フォルダを "unzip.py" などと同階層に作成する。

2. https://github.com/attardi/wikiextractor から WikiExtractor.py をダウンロードして "script/" に保存する。

3. https://dumps.wikimedia.org/jawiki から jawiki-latest-pages-articles.xml.bz2 をダウンロードして "data/" に保存する。

4. ウィキペディアコーパスを解凍して記事のみを抽出し、一つのファイルにまとめたコーパスが "data/" に保存される。
    ```
    $ python unzip.py
    ```
    保存されるファイル名は、 "config/config.yml" に保存した名前になる。

5. 解凍した記事を形態素解析して、様々な正規化処理を施したウィキペディア記事コーパスが "wakati/" に保存される。
    ```
    $ python wakati.py
    ```
    実行後に以下のように出力される。
    ```
    (ファイル名): (正規化前の文章数) -> (正規化後の文章数) -> (文単位に分割したときの文数)
    ```

6. 形態素解析したウィキペディア記事コーパスを、長さでフィルタリングしたコーパスが "filtered/" に保存される。
    ```
    $ python filter.py
    ```
    フィルタリングの内容は、 "config/config.yml" を編集することで変更できる。
    フィルタリング後に以下のように出力される。
    ```
    (ファイル名): (フィルタリング前のデータ数) -> (フィルタリング後のデータ数)
    ```

7. 形態素解析後のウィキペディア記事コーパスをすべて削除する。
    ```
    $ python clear.py
    ```
    オリジナルコーパスおよび解凍後のコーパスはダウンロードに非常に時間がかかるため削除しないようにしている。

## 設定
"config/config.yml" の各値の説明は以下の通り。

- filename: 保存されるファイルの名前 (文字列)
    - wiki_file: ウィキペディアコーパス
- filter: フィルタリングの内容 (整数)
    - len_min: 全体の長さの最小
    - len_max: 全体の長さの最大
