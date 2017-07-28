import os
import sys
import codecs
# import jieba

NEW_LINE = '\r\n'

def loadDocs(filePath, encoding='utf-8'):
    f = codecs.open(filePath, 'r', encoding=encoding)
    content = f.read()
    f.close()
    text_list = content.strip().split(NEW_LINE)
    text_list.remove( text_list[-1] )
    # for i in range(0, len(text_list)):
    #     text_list[i] = text_list[i].strip()
    return text_list


if __name__ == '__main__':
    pos_num = 0
    unlabel_num = 0
    test_num = 0

    word_set = set()

    text_list = loadDocs('./Lpu_Input/yuliao_pos.nlpresult')
    i = 0
    for doc in text_list:
        parts = doc.split('|')
        words = parts[-1].strip().split(' ')
        for word in words:
            word_set.add(word)
        print('process pos', i)
        i += 1

    text_list = loadDocs('./Lpu_Input/yuliao_unlabel.nlpresult')
    i = 0
    for doc in text_list:
        parts = doc.split('|')
        words = parts[-1].strip().split(' ')
        for word in words:
            word_set.add(word)
        print('process unlabel', i)
        i += 1

    text_list = loadDocs('./Lpu_Input/yuliao_test.nlpresult')
    i = 0
    for doc in text_list:
        parts = doc.split('|')
        words = parts[-1].strip().split(' ')
        for word in words:
            word_set.add(word)
        print('process test', i)
        i += 1


    # 写入临时词库文件
    fw = codecs.open('./data/Word_Library.wordlib', 'w', encoding='utf-8')

    word_lib = list(word_set)
    word_lib.sort()
    # while '' in word_lib:
    #     word_lib.remove('')
    # print(word_lib[0] + 'Done')

    
    for i in range(0, len(word_lib)):
        fw.write( word_lib[i].strip() + ' ' + str(i + 1) + NEW_LINE)
        print('writing word', i)

    fw.close()
    
    # 写入临时词库文件

