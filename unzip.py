##################################################
# ウィキペディア記事を解凍して一つにまとめる
# 実装開始日: 2019/4/14
# 実装完了日: 2019/4/14
# 実行方法: $ python unzip.py
# 備考: Linux環境を想定
##################################################

# 必要なモジュールのインポート
import os

# 各ファイルのパス
wiki_xml_path = "data/jawiki-latest-pages-articles.xml.bz2"
wiki_text_path = "data/wiki.txt"

# ウィキペディアのXMLファイルを解凍
os.system("python script/wikiExtractor.py " + wiki_xml_path + " --output data/tmp/")

# 解凍したファイルを一つにまとめて元データは削除する
os.system("find data/tmp/ | grep wiki | awk \'{system(\"cat \"$0\" >> " + wiki_text_path + "\")}\'")
os.system("rm -rf data/tmp/")
