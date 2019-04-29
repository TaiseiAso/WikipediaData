# coding: utf-8

"""
ウィキペディア記事を分かち書きしたコーパスに整形する
nkfツールが必要
"""
__author__ = "Aso Taisei"
__version__ = "1.0.0"
__date__ = "24 Apr 2019"


# 必要なモジュールのインポート
import yaml
import re
import os
import unicodedata
import MeCab


# 分かち書きするモジュール
tagger = MeCab.Tagger('-Ochasen')


class WikipediaProcessor():
    """ウィキペディア記事コーパスを加工するクラス"""
    def __init__(self, config):
        """
        コンストラクタ
        @param config 設定ファイル情報
        """
        pass

    def check(self, text):
        """
        テキストに不適切な情報が含まれていないかを判定
        @param text テキスト
        @return True: 適切、False: 不適切
        """
        # 英数字や特定の記号を含む
        if re.compile("^<|[a-zA-Z0-9]").search(text):
            return False
        # 特定のネットスラングを含む
        if re.compile("ナカーマ|イキスギ|いきすぎ|スヤァ|すやぁ|うぇーい|ウェーイ|おなしゃす|アザッス|あざっす|ドヤ|どや|ワカリミ|わかりみ").search(text):
            return False
        return True

    def normalize(self, text):
        """
        テキストに正規化などのフィルタ処理を行う
        @param text テキスト
        @return フィルタ処理を施したテキスト
        """
        text = re.sub("\([^笑泣嬉悲驚汗爆渋苦困死楽怒哀呆殴涙藁]+?\)", " ", text)
        text = re.sub("[^ぁ-んァ-ヶｧ-ｳﾞ一-龠々ー～〜、。！？!?,，.．]", " ", text)

        text = re.sub("[,，]", "、", text)
        text = re.sub("[．.]", "。", text)
        text = re.sub("〜", "～", text)
        text = re.sub("、(\s*、)+|。(\s*。)+", "...", text)

        text = re.sub("!+", "！", text)
        text = re.sub("！(\s*！)+", "！", text)
        text = re.sub("\?+", "？", text)
        text = re.sub("？(\s*？)+", "？", text)

        text = re.sub("～(\s*～)+", "～", text)
        text = re.sub("ー(\s*ー)+", "ー", text)

        text += "。"
        text = re.sub("[、。](\s*[、。])+", "。", text)

        text = re.sub("[。、！](\s*[。、！])+", "！", text)
        text = re.sub("[。、？](\s*[。、？])+", "？", text)
        text = re.sub("((！\s*)+？|(？\s*)+！)(\s*[！？])*", "!?", text)

        for w in ["っ", "笑", "泣", "嬉", "悲", "驚", "汗", "爆", "渋", "苦", "困", "死", "楽", "怒", "哀", "呆", "殴", "涙", "藁"]:
            text = re.sub(w + "(\s*" + w + ")+", " " + w + " ", text)

        text = re.sub("、\s*([笑泣嬉悲驚汗爆渋苦困死楽怒哀呆殴涙藁])\s*。", " \\1。", text)
        text = re.sub("(。|！|？|!\?)\s*([笑泣嬉悲驚汗爆渋苦困死楽怒哀呆殴涙藁])\s*。", " \\2\\1", text)

        text = re.sub("、", " 、 ", text)
        text = re.sub("。", " 。\n", text)

        text = re.sub("(\.\s*)+", " ... ", text)
        text = re.sub("！", " ！\n", text)
        text = re.sub("？", " ？\n", text)
        text = re.sub("!\?", " !?\n", text)

        text = re.sub("\n(\s*[～ー])+", "\n", text)

        text = re.sub("^([\s\n]*[。、！？!?ー～]+)+", "", text)
        text = re.sub("(.+?)\\1{3,}", "\\1\\1\\1", text)

        return text

    def del_morpheme(self, text):
        """
        テキストから特定の形態素を除去する
        @param text テキスト
        @return 特定の形態素を除去したテキストを文単位に分割したリスト
        """
        lines = text.strip().split("\n")
        results = []

        for line in lines:
            result = ""
            morphemes = tagger.parse(line).strip().split()

            for morpheme in morphemes:
                if morpheme not in ["ノ", "ーノ", "ロ", "艸", "屮", "罒", "灬", "彡", "ヮ", "益",\
                "皿", "タヒ", "厂", "厂厂", "啞", "卍", "ノノ", "ノノノ", "ノシ", "ノツ",\
                "癶", "癶癶", "乁", "乁厂", "マ", "んご", "んゴ", "ンゴ", "にき", "ニキ", "ナカ", "み", "ミ"]:
                    if morpheme not in ["つ", "っ"] or result != "":
                        result += morpheme + " "

            result = result.strip()
            if result not in ["、", "。", "！", "？", "!?", "", "... 。", "... ！", "... ？", "... !?",\
            "人 。", "つ 。", "っ 。", "笑 。", "笑 ！", "笑 ？", "笑 !?"]:
                results.append(result)

        return results


############


def wakati(config):
    """
    ウィキペディア記事を分かち書きしたコーパスを作成する
    @param config 設定ファイル情報
    """
    # 各ファイルのパス
    fn = config['filename']['wiki_file']
    wiki_path = "data/" + fn + ".txt"
    wiki_wakati_path = "wakati/" + fn + ".txt"

    if not os.path.isdir("data"):
        print("no data folder")
        return

    if not os.path.isfile(wiki_path):
        print("no " + wiki_path + " file")
        return

    # wakatiフォルダがなければ作成する
    if not os.path.isdir("wakati"):
        os.mkdir("wakati")

    # wakatiフォルダ内のファイルをすべて削除
    for root, _, files in os.walk("wakati", topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))

    cnt, cnt_, cnt_2 = 0, 0, 0

    # 形態素解析してコーパスを作成
    with open(wiki_path, 'r', encoding='utf-8') as f_text,\
    open(wiki_wakati_path, 'w', encoding='utf-8') as f_wakati:

        line = f_text.readline()
        while line:
            cnt += 1
            line = unicodedata.normalize('NFKC', line).strip()

            # 適切な文のみ選択する
            if check(line):
                # 文を整形して保存
                results = del_morpheme(normalize(line))
                if results != []:
                    cnt_ += 1
                for result in results:
                    cnt_2 += 1
                    f_wakati.write(result + "\n")

            line = f_text.readline()

    print(fn + ".txt: " + str(cnt) + " -> " + str(cnt_) + " -> " + str(cnt_2))

    # utf-8にする
    os.system("nkf -w --overwrite " + wiki_wakati_path)


if __name__ == '__main__':
    # 設定ファイルを読み込む
    config = yaml.load(stream=open("config/config.yml", 'rt'), Loader=yaml.SafeLoader)

    # ウィキペディア記事の分かち書きコーパスを作成
    wakati(config)
