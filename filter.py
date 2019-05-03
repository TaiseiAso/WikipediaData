# coding: utf-8

"""ウィキペディアデータをフィルタリング"""
__author__ = "Aso Taisei"
__version__ = "1.0.1"
__date__ = "4 May 2019"


# 必要なモジュールをインポート
import os
import yaml


class WikipediaFilter():
    """ウィキペディアコーパスをフィルタリングするためのクラス"""
    def __init__(self, config):
        """
        コンストラクタ
        @param config 設定ファイルの情報
        """
        # 保存ファイル名の情報取得
        fn = config['filename']
        self.wik_fn = fn['wiki_file']
        std_fn = fn['standard_file']
        prt_fn = fn['part_file']

        # 保存ファイルパス
        self.txt_fp = self.wik_fn + ".txt"
        self.std_fp = self.wik_fn + "_" + std_fn + ".txt"
        self.prt_fp = self.wik_fn + "_" + prt_fn + ".txt"

        # フィルタリング内容を取得
        fi = config['filter']
        fi_len = fi['length']
        self.len_min = fi_len['len_min']
        self.len_max = fi_len['len_max']

        fi_dp = fi['dump']
        self.dump_list = [
            fi_dp['noun'], fi_dp['verb'], fi_dp['adjective'],
            fi_dp['adverb'], fi_dp['particle'], fi_dp['auxiliary_verb'],
            fi_dp['conjunction'], fi_dp['prefix'], fi_dp['filler'],
            fi_dp['impression_verb'], fi_dp['three_dots'], fi_dp['phrase_point'],
            fi_dp['reading_point'], fi_dp['other']
        ]

        fi_ex = fi['exist']
        self.exist_list = [
            fi_ex['noun'], fi_ex['verb'], fi_ex['adjective'],
            fi_ex['adverb'], fi_ex['particle'], fi_ex['auxiliary_verb'],
            fi_ex['conjunction'], fi_ex['prefix'], fi_ex['filler'],
            fi_ex['impression_verb'], fi_ex['three_dots'], fi_ex['phrase_point'],
            fi_ex['reading_point']
        ]

        # 品詞のトークンを取得
        pt = config['part']
        self.token_list = [
            pt['noun'], pt['verb'], pt['adjective'],
            pt['adverb'], pt['particle'], pt['auxiliary_verb'],
            pt['conjunction'], pt['prefix'], pt['filler'],
            pt['impression_verb'], pt['three_dots'], pt['phrase_point'],
            pt['reading_point'], pt['other']
        ]

    def text_check(self, text):
        """
        テキストをフィルタリングする
        @param text 空白で分かち書きされたテキスト
        @return True: 適切、False: 不適切
        """
        length = len(text.strip().split())
        if self.len_min <= length and length <= self.len_max:
            return True
        return False

    def part_check(self, part):
        """
        品詞列をフィルタリングする
        @param part 品詞列
        @return True: 適切、False: 不適切
        """
        parts = part.strip().split()
        for exist, token in zip(self.exist_list, self.token_list):
            if exist and token not in parts:
                return False
        return True

    def del_part(self, text, standard, part):
        """
        指定した品詞のみを除去する
        @param text 空白で分かち書きされたテキスト
        @param standard 標準形/表層形のテキスト
        @param part 品詞列
        @return 品詞除去されたテキスト
        @return 品詞除去された標準形/表層形のテキスト
        @return 品詞除去された品詞列
        """
        result_text, result_standard, result_part = "", "", ""
        words, standards, parts = text.strip().split(), standard.strip().split() if standard else None, part.strip().split()

        if standards:
            for word, standard, part in zip(words, standards, parts):
                if part in self.token_list:
                    part_idx = self.token_list.index(part)
                    if self.dump_list[part_idx]:
                        result_text += word + " "
                        result_standard += standard + " "
                        result_part += part + " "
        else:
            for word, part in zip(words, parts):
                if part in self.token_list:
                    part_idx = self.token_list.index(part)
                    if self.dump_list[part_idx]:
                        result_text += word + " "
                        result_part += part + " "

        return result_text.strip() + "\n", result_standard.strip() + "\n" if standards else None, result_part.strip() + "\n"

    def filtering(self):
        """保存してあるすべてのコーパスをフィルタリングする"""
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
        if os.path.isfile("wakati/" + self.txt_fp):
            cnt, cnt_ = 0, 0

            # ファイルを開く
            f_txt = open("wakati/" + self.txt_fp, 'r', encoding='utf-8')
            f_txt_fi = open("filtered/" + self.txt_fp, 'w', encoding='utf-8')

            if os.path.isfile("wakati/" + self.std_fp):
                std = True
                f_std = open("wakati/" + self.std_fp, 'r', encoding='utf-8')
                f_std_fi = open("filtered/" + self.std_fp, 'w', encoding='utf-8')
            else:
                std = False

            if os.path.isfile("wakati/" + self.prt_fp):
                prt = True
                f_prt = open("wakati/" + self.prt_fp, 'r', encoding='utf-8')
                f_prt_fi = open("filtered/" + self.prt_fp, 'w', encoding='utf-8')
            else:
                prt = False

            # ファイルから読み込む
            line_txt = f_txt.readline()
            line_std = f_std.readline() if std else None
            line_prt = f_prt.readline() if prt else None

            while line_txt:
                cnt += 1

                # 指定した品詞を除外
                if prt:
                    line_txt, line_std, line_prt = self.del_part(line_txt, line_std if std else None, line_prt)

                # 適切なデータであるか判定
                if self.text_check(line_txt) and (not prt or self.part_check(line_prt)):
                    cnt_ += 1

                    # ファイルに書き込む
                    f_txt_fi.write(line_txt)
                    if std:
                        f_std_fi.write(line_std)
                    if prt:
                        f_prt_fi.write(line_prt)

                # ファイルから読み込む
                line_txt = f_txt.readline()
                line_std = f_std.readline() if std else None
                line_prt = f_prt.readline() if prt else None

            # ファイルを閉じる
            f_txt.close()
            f_txt_fi.close()
            if std:
                f_std.close()
                f_std_fi.close()
            if prt:
                f_prt.close()
                f_prt_fi.close()

            print(self.wik_fn + ".txt: " + str(cnt) + " -> " + str(cnt_))
        else:
            print("no filtered file")


def filtering_wikipedia_corpus(config):
    """
    ウィキペディアデータをフィルタリング
    @param config 設定ファイルの情報
    """
    f = WikipediaFilter(config)
    f.filtering()


if __name__ == '__main__':
    # 設定ファイルを読み込む
    config = yaml.load(stream=open("config/config.yml", 'rt'), Loader=yaml.SafeLoader)

    # フィルタ処理開始
    filtering_wikipedia_corpus(config)
