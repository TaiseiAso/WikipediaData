# coding: utf-8

"""ウィキペディア記事を解凍して一つにまとめる"""
__author__ = "Aso Taisei"
__version__ = "1.0.0"
__date__ = "24 Apr 2019"


# 必要なモジュールのインポート
import os


def unzip(config):
    """
    ウィキペディアのXMLファイルを解凍してすべてを一つにまとめる
    @param config 設定ファイル情報
    """
    # 各ファイルのパス
    extractor = "script/WikiExtractor.py"
    wiki_xml_path = "data/jawiki-latest-pages-articles.xml.bz2"
    wiki_path = "data/" + config['filename']['wiki_file'] + ".txt"

    if not os.path.isdir("data"):
        print("no data folder")
        return

    if not os.path.isdir("script"):
        print("no script folder")
        return

    if not os.path.isfile(extractor):
        print("no " + extractor + " file")
        return

    if not os.path.isfile(wiki_xml_path):
        print("no " + wiki_xml_path + " file")

    # ウィキペディアのXMLファイルを解凍
    os.system("python " + extractor + " " + wiki_xml_path + " --output data/tmp/")

    # 解凍したファイルを一つにまとめて元データは削除する
    os.system("find data/tmp/ | grep wiki | awk \'{system(\"cat \"$0\" >> " + wiki_path + "\")}\'")
    os.system("rm -rf data/tmp/")


if __name__ == '__main__':
    # 設定ファイルを読み込む
    config = yaml.load(stream=open("config/config.yml", 'rt'), Loader=yaml.SafeLoader)

    # 記事を解凍
    unzip(config)
