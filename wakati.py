##################################################
# ウィキペディア記事を分かち書きしたコーパスに整形する
# 実装開始日: 2019/4/14
# 実装完了日: 2019/4/15
# 実行方法: $ python wakati.py
# 備考: nkfツールのバイナリファイルが必要
##################################################

# 必要なモジュールのインポート
import re, os, unicodedata
import MeCab

# 分かち書きをするモジュール
owakati = MeCab.Tagger("-Owakati")

# 各ファイルのパス
if not os.path.isdir("data"):
    os.mkdir("data")
wiki_text_path = "data/wiki.txt"
wiki_wakati_path = "data/wiki_wakati.txt"

# 除外するパターン
rm = re.compile("^<|[a-zA-Z0-9_]")

# 形態素解析して単語の分散表現を学習するためのコーパスを作成
with open(wiki_text_path, 'r', encoding='utf-8') as f_text,\
open(wiki_wakati_path, 'w', encoding='utf-8') as f_wakati:

    line = f_text.readline()
    while line:
        line = unicodedata.normalize('NFKC', line).strip()

        # タグや英数字を含む場合は除外する
        while rm.search(line):
            line = f_text.readline()

        # 文を整形
        line = re.sub("\([^笑泣嬉悲驚汗爆渋苦困死楽怒哀呆殴涙藁]+?\)", " ", line)
        line = re.sub("[^ぁ-んァ-ヶｧ-ｳﾞ一-龠々ー～〜、。！？!?,，.．]", " ", line)

        line = re.sub("[,，]", "、", line)
        line = re.sub("[．.]", "。", line)
        line = re.sub("〜", "～", line)
        line = re.sub("、(\s*、)+|。(\s*。)+", "...", line)

        line = re.sub("!+", "！", line)
        line = re.sub("！(\s*！)+", "！", line)
        line = re.sub("\?+", "？", line)
        line = re.sub("？(\s*？)+", "？", line)

        line = re.sub("～(\s*～)+", "～", line)
        line = re.sub("ー(\s*ー)+", "ー", line)

        line += "。"
        line = re.sub("[、。](\s*[、。])+", "。", line)

        line = re.sub("[。、！](\s*[。、！])+", "！", line)
        line = re.sub("[。、？](\s*[。、？])+", "？", line)
        line = re.sub("((！\s*)+？|(？\s*)+！)(\s*[！？])*", "!?", line)

        for w in ["っ", "笑", "泣", "嬉", "悲", "驚", "汗", "爆", "渋", "苦", "困", "死", "楽", "怒", "哀", "呆", "殴", "涙", "藁"]:
            line = re.sub(w + "(\s*" + w + ")+", " " + w + " ", line)

        line = re.sub("、\s*([笑泣嬉悲驚汗爆渋苦困死楽怒哀呆殴涙藁])\s*。", " \\1。", line)
        line = re.sub("(。|！|？|!\?)\s*([笑泣嬉悲驚汗爆渋苦困死楽怒哀呆殴涙藁])\s*。", " \\2\\1", line)

        line = re.sub("、", " 、 ", line)
        line = re.sub("。", " 。\n", line)
        # 、。を除去する場合
        #line = re.sub("、", " ", line)
        #line = re.sub("。", "\n", line)

        line = re.sub("(\.\s*)+", " ... ", line)
        line = re.sub("！", " ！\n", line)
        line = re.sub("？", " ？\n", line)
        line = re.sub("!\?", " !?\n", line)

        line = re.sub("\n(\s*[～ー])+", "\n", line)

        line = re.sub("^([\s\n]*[。、！？!?ー～]+)+", "", line)
        line = re.sub("(.+?)\\1{3,}", "\\1\\1\\1", line)

        # 改行ごとに文を分割する
        for sent in line.split("\n"):
            add_sent = ""
            words = owakati.parse(sent).strip().split()
            for word in words:
                if word not in ["ノ", "ーノ", "ロ", "艸", "屮", "罒", "灬", "彡", "ヮ", "益",\
                "皿", "タヒ", "厂" ,"厂厂", "啞", "卍", "ノノ", "ノノノ", "ノシ", "ノツ",\
                "癶", "癶癶", "乁", "乁厂", "マ", "んご", "んゴ", "ンゴ", "にき", "ニキ", "ナカ", "み", "ミ"]:
                    if word not in ["つ", "っ"] or add_sent != "":
                        add_sent += word + " "

            add_sent = add_sent.strip()
            if add_sent not in ["、", "。", "！", "？", "!?", "", "... 。", "... ！", "... ？", "... !?",\
            "人 。", "つ 。", "っ 。", "笑 。", "笑 ！", "笑 ？", "笑 !?"]:
                f_wakati.write(add_sent + "\n")

        line = f_text.readline()

# utf-8にする
os.system("nkf -w --overwrite " + wiki_wakati_path)
