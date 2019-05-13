# coding: utf-8

"""
ウィキペディア記事を分かち書きしたコーパスに整形する
nkfツールが必要
"""
__author__ = "Aso Taisei"
__version__ = "1.0.1"
__date__ = "4 May 2019"


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
        # 保存ファイル名の情報取得
        fn = config['filename']
        self.wik_fn = fn['wiki_file']
        std_fn = fn['standard_file']
        prt_fn = fn['part_file']

        # 保存ファイルパス
        self.wik_fp = "data/" + self.wik_fn + ".txt"
        self.txt_fp = "wakati/" + self.wik_fn + ".txt"
        self.std_fp = "wakati/" + self.wik_fn + "_" + std_fn + ".txt"
        self.prt_fp = "wakati/" + self.wik_fn + "_" + prt_fn + ".txt"

        # 保存するかどうかを取得
        fd = config['dump']
        self.std_fd = fd['standard_file']
        self.prt_fd = fd['part_file']

        # 品詞のトークンを取得
        pt = config['part']
        self.noun_main_token = pt['noun_main']
        self.noun_sub_token = pt['noun_sub']
        self.verb_main_token = pt['verb_main']
        self.verb_sub_token = pt['verb_sub']
        self.adjective_main_token = pt['adjective_main']
        self.adjective_sub_token = pt['adjective_sub']
        self.adverb_token = pt['adverb']
        self.particle_token = pt['particle']
        self.auxiliary_verb_token = pt['auxiliary_verb']
        self.conjunction_token = pt['conjunction']
        self.prefix_token = pt['prefix']
        self.filler_token = pt['filler']
        self.impression_verb_token = pt['impression_verb']
        self.three_dots_token = pt['three_dots']
        self.phrase_point_token = pt['phrase_point']
        self.reading_point_token = pt['reading_point']
        self.other_token = pt['other']

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
        if re.compile("ナカーマ|イキスギ|いきすぎ|スヤ|すや|うぇーい|ウェーイ|おなしゃす|アザッス|あざっす|ドヤ|どや|ワカリミ|わかりみ|分かりみ").search(text):
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
        @return 特定の形態素を除去したテキストのリスト
        @return 標準形/表層系のテキストのリスト
        @return 品詞列のリスト
        """
        lines = text.strip().split("\n")
        results, standards, parts = [], [], []

        for line in lines:
            add_result, add_standard, add_part = "", "", ""
            node = tagger.parseToNode(line)

            while node:
                feature = node.feature.split(',')
                if feature[0] == "BOS/EOS":
                    node = node.next
                    continue

                if node.surface in [".", "..", "!", "?", "ノ", "ーノ", "ロ", "艸", "屮", "罒", "灬", "彡", "ヮ", "益",\
                "皿", "タヒ", "厂", "厂厂", "啞", "卍", "ノノ", "ノノノ", "ノシ", "ノツ",\
                "癶", "癶癶", "乁", "乁厂", "マ", "んご", "んゴ", "ンゴ", "にき", "ニキ", "ナカ", "み", "ミ"]:
                    node = node.next
                    continue

                if node.surface in ["つ", "っ"] and add_result == "":
                    node = node.next
                    continue

                if feature[0] == "名詞":
                    if feature[1] in ["サ変接続", "一般", "形容動詞語幹", "固有名詞"]:
                        token = self.noun_main_token
                    else:
                        token = self.noun_sub_token
                elif feature[0] == "動詞":
                    if feature[1] in ["自立"]:
                        token = self.verb_main_token
                    else:
                        token = self.verb_sub_token
                elif feature[0] == "形容詞":
                    if feature[1] in ["自立"]:
                        token = self.adjective_main_token
                    else:
                        token = self.adjective_sub_token
                elif feature[0] == "副詞":
                    token = self.adverb_token
                elif feature[0] == "助詞":
                    token = self.particle_token
                elif feature[0] == "助動詞":
                    token = self.auxiliary_verb_token
                elif feature[0] == "接続詞":
                    token = self.conjunction_token
                elif feature[0] == "接頭詞":
                    token = self.prefix_token
                elif feature[0] == "フィラー":
                    token = self.filler_token
                elif feature[0] == "感動詞":
                    token = self.impression_verb_token
                elif node.surface == "...":
                    token = self.three_dots_token
                elif node.surface in ["。", "！", "？", "!?"]:
                    token = self.phrase_point_token
                elif node.surface == "、":
                    token = self.reading_point_token
                else:
                    token = self.other_token

                add_result += node.surface + " "
                if re.compile("[^ぁ-んァ-ヶｧ-ｳﾞ一-龠々ー～]").search(feature[6]) or\
                token in [self.three_dots_token, self.phrase_point_token, self.reading_point_token] or\
                node.surface in ["ー", "～"]:
                    add_standard += node.surface + " "
                else:
                    add_standard += feature[6] + " "
                add_part += token + " "

                node = node.next

            if add_result.strip() not in ["、", "。", "！", "？", "!?", "", "... 。", "... ！", "... ？", "... !?",\
            "人 。", "つ 。", "っ 。", "笑 。", "笑 ！", "笑 ？", "笑 !?"]:
                results.append(add_result.strip())
                standards.append(add_standard.strip())
                parts.append(add_part.strip())

        return results, standards, parts

    def wakati(self):
        """ウィキペディア記事を分かち書きしたコーパスを作成する"""
        if not os.path.isdir("data"):
            print("no data folder")
            return

        if not os.path.isfile(self.wik_fp):
            print("no " + self.wik_fp + " file")
            return

        # wakatiフォルダがなければ作成する
        if not os.path.isdir("wakati"):
            os.mkdir("wakati")

        # wakatiフォルダ内のファイルをすべて削除
        for root, _, files in os.walk("wakati", topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))

        cnt, cnt_, cnt_2 = 0, 0, 0

        f_txt = open(self.txt_fp, 'w', encoding='utf-8')
        if self.std_fd:
            f_std = open(self.std_fp, 'w', encoding='utf-8')
        if self.prt_fd:
            f_prt = open(self.prt_fp, 'w', encoding='utf-8')

        # 形態素解析してコーパスを作成
        with open(self.wik_fp, 'r', encoding='utf-8') as f:

            line = f_text.readline()
            while line:
                cnt += 1
                line = unicodedata.normalize('NFKC', line).strip()

                # 適切な文のみ選択する
                if check(line):
                    # 文を整形して保存
                    results, standards, parts = self.del_morpheme(self.normalize(line))
                    if results != []:
                        cnt_ += 1
                        cnt_2 += len(results)

                        for result in results:
                            f_txt.write(result + "\n")
                        if self.std_fd:
                            for standard in standards:
                                f_std.write(standard + "\n")
                        if self.prt_fd:
                            for part in parts:
                                f_prt.write(part + "\n")

                line = f_text.readline()

        print(self.wik_fn + ".txt: " + str(cnt) + " -> " + str(cnt_) + " -> " + str(cnt_2))

        f_txt.close()
        if self.std_fd:
            f_std.close()
        if self.prt_fd:
            f_prt.close()

        # utf-8にする
        os.system("nkf -w --overwrite " + self.txt_fp)
        if self.std_fd:
            os.system("nkf -w --overwrite " + self.std_fp)
        if self.prt_fd:
            os.system("nkf -w --overwrite " + self.prt_fp)


def get_wikipedia_corpus(config):
    """
    ウィキペディアよりコーパスを作成
    @param config 設定ファイル情報
    """
    processor = WikipediaProcessor(config)
    processor.wakati()


if __name__ == '__main__':
    # 設定ファイルを読み込む
    config = yaml.load(stream=open("config/config.yml", 'rt', encoding='utf-8'), Loader=yaml.SafeLoader)

    # ウィキペディア記事の分かち書きコーパスを作成
    get_wikipedia_corpus(config)
