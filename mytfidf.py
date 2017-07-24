import jieba
import os
import sys
import codecs
import numpy as np
import math


# test
def myprint(mstr):
    print('haha', mstr)

# test


if __name__ == '__main__':
    pos_num = 0
    unlabel_num = 0
    word_set = set()


    # 小函数
    def cal_len(vec):
        vec = np.mat(vec)
        num = (float)(vec * vec.T)
        return math.sqrt(num)

    def norm(vec):
        vec = np.array(vec)
        return vec / cal_len(vec)
    # 小函数


    def loadDocs(filePath, encoding='utf-8'):
        f = codecs.open(filePath, 'r', encoding=encoding)
        content = f.read()
        f.close()
        text_list = content.split('\n')
        text_list.remove( text_list[-1] )
        for i in range(0, len(text_list)):
            text_list[i] = text_list[i].strip()
        return text_list


    # io 预备
    text_list = []
    # 读取 pos
    temp = loadDocs('./test/yuliao_pos.csv')
    pos_num = len(temp)
    text_list.extend(temp)
    # 读取 pos


    # 读取 unlabel
    temp = loadDocs('./test/yuliao_unlabel.csv')
    unlabel_num = len(temp)
    text_list.extend(temp)
    # 读取 unlabel

    print('pos:', pos_num, 'unlabel:', unlabel_num)
    # io 预备


    # 分词
    jieba.add_word('不喜欢')
    jieba.add_word('耗油')
    jieba.add_word('不合格')

    for i in range(0, len(text_list)):
        temp = text_list[i].split('|')
        text_list[i] = jieba.lcut( temp[-1], cut_all=False )
        # text_list[i] = list(seg_list)

    # 分词


    # 去停用词
    # 读取停用词
    f = codecs.open('./结巴分词/stop_word_UTF_8.txt', 'r', encoding='utf-8')
    content = f.read()
    f.close()
    stop_word_list = content.split('\r\n')
    stop_word_list.remove( stop_word_list[-1] )

    print(stop_word_list)
    # for i in range(0, len(stop_word_list)):
    #     print('#' + str(i) + '\t' + stop_word_list[i])
    # 读取停用词

    # f = open('./jieba_segment.txt', 'w', encoding='utf-8')

    for i in range(0, len(text_list)):
        j = 0
        while j < len(text_list[i]):
            if text_list[i][j] in stop_word_list:
                text_list[i].remove( text_list[i][j] )
            else:
                word_set.add( text_list[i][j] )
                j += 1
        # f.write(' '.join(text_list[i]) + '\n')
        # print('doc', i)

    # f.close()

    # for i in range(0, len(text_list)):
    #     print('#' + str(i) + '\t' + ' '.join(text_list[i]))
    # 去停用词


    # 词库排序
    word_set = list(word_set)
    word_set.sort()

    # print('word set:')
    # print(word_set)
    # 词库排序


    # test tfidf
    f = codecs.open('./test/word_set.txt', 'w', encoding='utf-8')
    word_num = len(word_set)
    id = 0
    for word in word_set:
        f.write( word + ' ' + str(id) + '\n' )
        id += 1
    f.close()

    # 计算 tf
    weight = [ [] for i in range(0, len(text_list)) ]
    for i in range(0, len(text_list)):
        weight[i] = [0 for j in range(0, word_num)]
        for word in text_list[i]:
            weight[i][ word_set.index(word) ] += 1

        cnt = len(text_list[i])
        if cnt != 0:
            for j in range(0, len(weight[i])):
                weight[i][j] /= cnt
        # print('weight', i)
    # 计算 tf

    D_num = len(text_list)
    for i in range(0, len(text_list)):
        for j in range(0, len(text_list[i])):
            if weight[i][j] != 0:
                cnt = 0
                for doc in text_list:
                    if word_set[j] in doc:
                        cnt += 1
                idf = math.log( D_num / cnt) + 1
                weight[i][j] *= idf
        # print('process doc', i)        

    for i in range(0, len(weight)):
        weight[i] = np.array(norm(weight[i]))
        weight[i] = weight[i].tolist()
        

    # for a in weight:
        # print(a, '\n')


    # f = open('./testtfidf.txt', 'w', encoding='utf-8')
    # for a in weight:
    #     mstr = ''
    #     for b in a:
    #         mstr += str(b) + ' '
    #     # print(mstr)
    #     f.write(mstr.strip() + '\n')
    # f.close()

    f = codecs.open("./test/tfidf.txt", 'w', encoding = "utf-8")
    for i in range(0, len(weight)): #打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
        out_str = ''
        for j in range(0, len(weight[i])):
            out_str += word_set[j] + ':' + str(weight[i][j]) + ' '
        f.write(out_str.strip() + '\n')
    f.close()
    # test tfidf
