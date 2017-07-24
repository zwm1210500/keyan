# import os




# if __name__ == '__main__':
#     pos_file_path = './data/yuliao.pos'
#     unlabel_file_path = './data/yuliao.unlabel'

#     pos_file = open(pos_file_path, 'r')
#     unlabel_file = open(unlabel_file_path, 'r')

#     pos_docs = pos_file.read()
#     unlabel_docs = unlabel_file.read()

#     pos_list = pos_docs.split('\n')
#     unlabel_list = unlabel_docs.split('\n')
#     # 去掉最后一个元素（空字符串）
#     pos_list.remove(pos_list[-1])
#     unlabel_list.remove(unlabel_list[-1])
#     # 去掉最后一个元素（空字符串）

#     for i in range(0, len(pos_list)):
#         pos_list[i] = str(pos_list[i]).strip().split(' ')
#         for j in range(0, len(pos_list[i])):
#             pos_list[i][j] = pos_list[i][j].split(':')

#     for i in range(0, len(unlabel_list)):
#         unlabel_list[i] = str(unlabel_list[i]).strip().split(' ')
#         for j in range(0, len(unlabel_list[i])):
#             unlabel_list[i][j] = unlabel_list[i][j].split(':')




# prepare
import codecs
import jieba

if __name__ == '__main__':
    pos_file = codecs.open('./data/yuliao_pos.csv', 'r', 'utf-8')
    # unlabel_file = codecs.open('./data/yuliao_unlabel.csv', 'r', 'utf-8')

    pos_content = pos_file.read()

    list = pos_content.split('\r\n')
    for i in range(0, len(list)):
        list[i] = list[i].split('|')
        list[i] = list[0]


    print(list[0][3])




    print('Done')