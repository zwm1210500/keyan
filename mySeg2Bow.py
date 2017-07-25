import os
import codecs


def loadDocs(filePath, encoding='utf-8'):
    f = codecs.open(filePath, 'r', encoding=encoding)
    content = f.read()
    f.close()
    text_list = str(content).split('\n')
    text_list.remove( text_list[-1] )
    for i in range(0, len(text_list)):
        text_list[i] = text_list[i].strip()
    return text_list

def loadWordLib(filePath, encoding='utf-8'):
    f = codecs.open(filePath, 'r', encoding=encoding)
    content = f.read()
    f.close()
    text_list = content.split('\n')
    word2id = {}
    for word_id in text_list:
        parts = word_id.split(' ')
        word2id[word_id[0]] = word_id[1]
    return word2id


def transform(words):
    word_set = set()
    for word in words:
        word_set.add(word)
    word_list = list(word_set)
    for i in range(0, len(word_list)):
        word_list[i] = word2id[ word_list[i] ]
    word_list.sort()
    for i in range(0, len(word_list)):
        


if __name__ == '__main__':
    word2id = loadWordLib('./data/Word_Library.wordlib')

    text_list = loadDocs('./Lpu_Input/yuliao_pos.nlpresult')
    i = 0
    for doc in text_list:
        doc = doc.split('|')
        word_set = set()
        words = doc[-1].split(' ')

        

