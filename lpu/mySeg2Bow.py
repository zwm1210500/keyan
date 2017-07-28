import os
import codecs

NEW_LINE = '\r\n'

def toset(mlist):
    temp = set()
    for elem in mlist:
        temp.add(elem)
    return temp

def loadDocs(filePath, encoding='utf-8'):
    f = codecs.open(filePath, 'r', encoding=encoding)
    content = f.read()
    f.close()
    text_list = content.split(NEW_LINE)
    text_list.remove( text_list[-1] )
    # for i in range(0, len(text_list)):
    #     text_list[i] = text_list[i].strip()
    return text_list

def loadWordLib(filePath, encoding='utf-8'):
    f = codecs.open(filePath, 'r', encoding=encoding)
    content = f.read()
    f.close()
    text_list = content.split(NEW_LINE)
    text_list.remove( text_list[-1] )
    word2id = {}
    for word_id in text_list:
        parts = word_id.split(' ')
        word2id[parts[0]] = int(parts[1])
    return word2id


# def transform(words):
#     word_set = set()
#     for word in words:
#         word_set.add(word)
#     word_list = list(word_set)
#     for i in range(0, len(word_list)):
#         word_list[i] = word2id[ word_list[i] ]
#     word_list.sort()
#     for i in range(0, len(word_list)):
        


if __name__ == '__main__':
    word2id = loadWordLib('./data/Word_Library.wordlib')

    text_list = loadDocs('./Lpu_Input/yuliao_pos.nlpresult')
    fw = codecs.open('./Lpu_Input/yuliao.pos', 'w', 'utf-8')
    i = 0
    for doc in text_list:
        doc = doc.split('|')
        words = doc[-1].strip().split(' ')
        for j in range(0, len(words)):
            # print(str(i + 1) + ' ' + words[j])
            words[j] = word2id.get( words[j], 1 )
        word_set = toset(words)
        word_list = list(word_set)
        word_list.sort()
        out_str = ''
        for j in range(0, len(word_list)):
            # word_list[j] = str(word_list[j]) + ':' + str( words.count(word_list[j]) )
            out_str += str(word_list[j]) + ':' + str( words.count(word_list[j]) ) + ' '
        fw.write( out_str.strip() + NEW_LINE )
        print('writing pos', i)
        i += 1

    fw.close()
        

    text_list = loadDocs('./Lpu_Input/yuliao_unlabel.nlpresult')
    fw = codecs.open('./Lpu_Input/yuliao.unlabel', 'w', 'utf-8')
    i = 0
    for doc in text_list:
        doc = doc.split('|')
        words = doc[-1].strip().split(' ')
        for j in range(0, len(words)):
            # print(str(i + 1) + ' ' + words[j])
            words[j] = word2id.get( words[j], 1 )
        word_set = toset(words)
        word_list = list(word_set)
        word_list.sort()
        out_str = ''
        for j in range(0, len(word_list)):
            # word_list[j] = str(word_list[j]) + ':' + str( words.count(word_list[j]) )
            out_str += str(word_list[j]) + ':' + str( words.count(word_list[j]) ) + ' '
        fw.write( out_str.strip() + NEW_LINE )
        print('writing unlabel', i)
        i += 1

    fw.close()
        

    text_list = loadDocs('./Lpu_Input/yuliao_test.nlpresult')
    fw = codecs.open('./Lpu_Input/yuliao.test', 'w', 'utf-8')
    i = 0
    for doc in text_list:
        doc = doc.split('|')
        words = doc[-1].strip().split(' ')
        for j in range(0, len(words)):
            # print(str(i + 1) + ' ' + words[j])
            words[j] = word2id.get( words[j], 1 )
        word_set = toset(words)
        word_list = list(word_set)
        word_list.sort()
        out_str = str(doc[0]) + '|'
        for j in range(0, len(word_list)):
            # word_list[j] = str(word_list[j]) + ':' + str( words.count(word_list[j]) )
            out_str += str(word_list[j]) + ':' + str( words.count(word_list[j]) ) + ' '
        fw.write( out_str.strip() + NEW_LINE )
        print('writing test', i)
        i += 1

    fw.close()
        
        



