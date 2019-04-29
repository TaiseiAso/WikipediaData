# coding: utf-8

"""ウィキペディアデータを長さでフィルタリング"""
__author__ = "Aso Taisei"
__version__ = "1.0.0"
__date__ = "25 Apr 2019"


# 必要なモジュールをインポート
import os
import yaml


def check(line, fi):
    """
    テキストをフィルタ処理して適切かどうかを判定する
    @param line テキスト
    @param fi 設定ファイルのフィルタ処理内容の情報
    @return True: 適切、False: 不適切
    """
    length = len(line.strip().split())
    if fi['len_min'] <= length and length <= fi['len_max']:
        return True
    return False


def filtering(config):
    """
    保存してあるコーパスにフィルタ処理を施す
    @param config 設定ファイル情報
    """
    fn = config['filename']['wiki_file']
    fi = config['filter']

    # wakatiフォルダがなければ終了
    if not os.path.isdir("wakati"):
        print("no wakati folder")
        return

    # filteredフォルダがなければ作成する
    if not os.path.isdir("filtered"):
        os.mkdir("filtered")

    # filteredフォルダ内のファイルをすべて削除
    for root, _, files in os.walk("filtered", topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))

    # 分かち書きされたウィキペディアデータをフィルタリング
    if os.path.isfile("wakati/" + fn + ".txt"):
        cnt, cnt_ = 0, 0

        with open("wakati/" + fn + ".txt", 'r', encoding='utf-8') as f,\
        open("filtered/" + fn + ".txt", 'w', encoding='utf-8') as f_filtered:

            line = f.readline()

            while line:
                cnt += 1

                if check(line, fi):
                    cnt_ += 1
                    f_filtered.write(line)

                line = f.readline()

        print(fn + ".txt: " + str(cnt) + " -> " + str(cnt_))
    else:
        print("no filtered file")


if __name__ == '__main__':
    # 設定ファイルを読み込む
    config = yaml.load(stream=open("config/config.yml", 'rt'), Loader=yaml.SafeLoader)

    # フィルタ処理開始
    filtering(config)
