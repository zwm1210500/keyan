import mySegment
import codecs

NEW_LINE = '\r\n'

if __name__ == '__main__':
    stop_word_list = mySegment.loadTYC()

    text_list = []
    fw = codecs.open('./InputFile/yuliao.txt', 'w', 'utf-8')

    pos_list = mySegment.loadDocs('./InputFile/yuliao_pos.csv')
    pos_list = mySegment.mySegment(pos_list)
    pos_list = mySegment.quTYC(pos_list, stop_word_list)
    text_list.extend(pos_list)

    unlabel_list = mySegment.loadDocs('./InputFile/yuliao_unlabel.csv')
    unlabel_list = mySegment.mySegment(unlabel_list)
    unlabel_list = mySegment.quTYC(unlabel_list, stop_word_list)
    text_list.extend(unlabel_list)

    test_list = mySegment.loadDocs('./InputFile/yuliao_test.csv')
    test_list = mySegment.mySegment(test_list)
    test_list = mySegment.quTYC(test_list, stop_word_list)
    text_list.extend(test_list)
    
    i = 0
    for doc in text_list:
        if doc[-1] != []:
            fw.write(' '.join(doc[-1]) + NEW_LINE)
            print('writing doc', i)
            i += 1

    fw.close()

