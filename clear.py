# coding: utf-8

"""ウィキペディアデータをすべて削除"""
__author__ = "Aso Taisei"
__version__ = "1.0.0"
__date__ = "25 Apr 2019"


# 必要なモジュールをインポート
import os


def clear(folders):
    """
    指定したフォルダの中のファイルをすべて削除
    @param folders 中身を削除するフォルダのリスト
    """
    for top in folders:
        for root, _, files in os.walk(top, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))


if __name__ == '__main__':
    clear(["data", "wakati", "filtered"])
