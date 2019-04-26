# coding: utf-8

"""形態素解析後のウィキペディアコーパスをすべて削除"""
__author__ = "Aso Taisei"
__version__ = "1.0.1"
__date__ = "26 Apr 2019"


# 必要なモジュールをインポート
import os


def delete(folders):
    """
    指定したフォルダをすべて削除する
    @param folders 削除するフォルダのリスト
    """
    for folder in folders:
        os.system("rm -rf " + folder)


if __name__ == '__main__':
    delete(["wakati", "filtered"])
