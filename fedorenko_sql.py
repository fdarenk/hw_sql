import urllib.request as ur, re, os, html
from flask import Flask, url_for, render_template, request, redirect

app = Flask(__name__)
@app.route('/')
def page():
    if request.args:
        create_inserts(request.args['text'], request.args['path'])
    return render_template('page.html')

def create_inserts(text, result_file):
    wordforms = {}
    words = mystemming(text).split(' ')
    print(words)
    num_in_text = 1
    for word in words:
        res_word = re.search('(\W*)([\w\-]*)\{(.*)\}(\W*)', word)
        punct_l = res_word.group(1).strip('\n\t')
        token = res_word.group(2).strip('\n\t')
        lemma = res_word.group(3).strip('\n\t')
        punct_r = res_word.group(4).strip('\n\t')
        wordform = token.lower()
        if wordform not in wordforms:
            wordforms[wordform] = [len(wordforms), lemma]
        write_insert_for_token(result_file, token, punct_r, punct_l, wordforms[wordform][0], num_in_text)
        num_in_text += 1
    for wordform in wordforms:
        write_insert_for_analysis(result_file, wordform, wordforms[wordform][0], wordforms[wordform][1])

def mystemming(input_text):
    file_in = open('input_text.txt', 'w', encoding = 'utf-8')
    file_in.write(input_text)
    file_in.close()
    os.system('./mystem -cd input_text.txt output.txt')
    file_out = open('output.txt', 'r', encoding = 'utf-8')
    output = file_out.read()
    file_out.close
    return output

def write_insert_for_token(result_file, token, punct_r, punct_l, analysis, num_in_text):
    file = open(result_file, 'a', encoding = 'utf-8')
    file.write('INSERT INTO tokens(token, punct_r, punct_l, analysis, num_in_text) VALUES(\"' + token + '\",\"' + punct_r + '\",\"' + punct_l + '\",' + str(analysis) + ',' + str(num_in_text) + ');\n')
    file.close()
#Предполагается, что столбик id в таблице с токенчиками заполняется автоматически с помощью галочки АИ

def write_insert_for_analysis(result_file, wordform, num_id, lemma):
    file = open(result_file, 'a', encoding = 'utf-8')
    file.write('INSERT INTO analyses(wordform, id, lemma) VALUES(\"' + wordform + '\",\"' + str(num_id) + '\",\"' + lemma + '\");\n')
    file.close()

if __name__ == '__main__':
    app.run()
