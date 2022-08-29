"""
A script for adding hiragana transcriptions to katakana in html. Seriously messes up the html, but appears to work.
"""
import argparse
from html.parser import HTMLParser
import os

kanas = """あア	かカ	さサ	たタ	なナ	はハ	まマ	やヤ	らラ	わワ    んン
いイ	きキ	しシ	ちチ	にニ	ひヒ	みミ	𛀆𛄠*	りリ	ゐヰ
うウ	くク	すス	つツ	ぬヌ	ふフ	むム	ゆユ	るル	𛄟𛄢*
えエ	けケ	せセ	てテ	ねネ	へヘ	めメ	𛀁𛄡*	れレ	ゑヱ
おオ	こコ	そソ	とト	のノ	ほホ	もモ	よヨ	ろロ	をヲ
がガ	ざザ	だダ	ばバ	ぱパ	か゚カ゚	ら゚ラ゚
ぎギ	じジ	ぢヂ	びビ	ぴピ	き゚キ゚	り゚リ゚
ぐグ	ずズ	づヅ	ぶブ	ぷプ	く゚ク゚	る゚ル゚
げゲ	ぜゼ	でデ	べベ	ぺペ	け゚ケ゚	れ゚レ゚
ごゴ	ぞゾ	どド	ぼボ	ぽポ	こ゚コ゚	ろ゚ロ゚
んン
あァ
いィ
うゥ
えェ
おォ
つッ
やャ
ゆュ
よョ
わヮ
かヵ
けヶ"""

# create katakana to hiragana dict
kanas = kanas.split('\n')

kdict = {}
for row in kanas:
    r = [x for x in row.split('\t') if '*' not in x]
    for c in r:
        kdict[c[1]] = c[0]

def contains_kata(data):
    for key in kdict:
        if key in data:
            return True
    return False

def get_kata_indices(data):
    indices = []
    for i, x in enumerate(data):
        if x in kdict:
            indices.append(i)
    
    ranges = []
    start = indices[0]
    last = indices[0]
    for i, x in enumerate(indices):
        if i == 0:
            continue
        if x - last == 1:
            last = x
        else:
            ranges.append([start, last])
            start = x
            last = x
        if i == len(indices) - 1:
            if not ranges or ranges[-1][-1] != last:
                ranges.append([start, last])
    return ranges

def get_hira(kata):
    hira = []
    for x in kata:
        hira.append(kdict[x])
    return ''.join(hira)
    
def update_file(filename, overwrite=False):
    with open(filename, 'r') as f:
        html = f.read()

    lines = html.split('\n')
    new_lines = []
    for line in lines:
        if contains_kata(line):
            new_line = line[:]
            indices = get_kata_indices(new_line)
            indices.reverse()
            for i in indices:
                if len(i) > 1:
                    kata = line[i[0]:i[1]+1]
                else:
                    kata = line[i[0]]
                hira = get_hira(kata)
                hira = f'<rt>{hira}</rt>'
                index = i[-1] + 1
                pre = i[0]
                new_line = new_line[:pre] + '<ruby>' + new_line[pre:index] + hira + '</ruby>' + new_line[index:]
            new_lines.append(new_line)
        else:
            new_lines.append(line)

    newfile = filename[:-5] + '_kanaed' + filename[-5:]
    if overwrite:
        newfile = filename

    with open(newfile, 'w') as f:
        f.write('\n'.join(new_lines))

def run():
    parser = argparse.ArgumentParser(description='Add hiragana transcriptions to katakana in html')
    parser.add_argument('filename', type=str, help='source file to update')
    parser.add_argument('--directory', action='store_true', help='specify directory instead of filename and update all files in directory')
    parser.add_argument('--overwrite', action='store_true', required=False, help='overwrite source file with changes')

    options = parser.parse_args()
    overwrite = True if options.overwrite else False
    if options.directory:
        for f in os.listdir(options.filename):
            if 'html' in f:
                filepath = os.path.join(options.filename, f)
                update_file(filepath, overwrite=overwrite)
    else:
        update_file(options.filename, overwrite=overwrite)

if __name__ == '__main__':
    run()
