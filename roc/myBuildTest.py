from myroc import *

NEW_LINE = '\r\n'

if __name__ == '__main__':
    word2vec = loadVector('./InputFile/vectors.txt')

    fr = codecs.open('./InputFile/yuliao_test.nlpresult', 'r', 'utf-8')
    content = fr.read()
    fr.close()
    test_title = []
    test_list = []
    temp_list = content.split(NEW_LINE)
    temp_list.remove(temp_list[-1])
    for doc in temp_list:
        parts = doc.split('|')
        test_title.append(parts[0])
        test_list.append(parts[-1])
    test_vector = toVector(test_list, word2vec)

    for i in range(0, len(test_vector)):
        test_vector[i] = (np.array(test_vector[i]).tolist())[0]

    fw = codecs.open('../svm/test.txt', 'w', 'utf-8')
    a = 0
    for doc in test_vector:
        out_str = test_title[a]
        for i in range(0, len(doc)):
            if doc[i] != 0:
                out_str += ' ' + str(i + 1) + ':' + str(doc[i])
        if out_str != test_title[a]:
            fw.write(out_str)
            fw.write(NEW_LINE)
            print('write test', a + 1)
            a += 1
    fw.close()