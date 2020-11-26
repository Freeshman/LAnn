#!/usr/bin/python
#coding = utf8
"""
# Author: hu-tom
# Created Time : 2020-02-24 18:46:36

# File Name: LAnn_NER.py
# Description:

"""
import os
from pylab import *
result = 'result/'
if not os.path.exists(result):
    os.mkdir(result)
lann_dir = ''
fs = os.listdir()
txts = [i for i in fs if i[-5:] == '.lann']
datas = []
labels = []
statitic = []
chars_count = 0
entity_count = 0
char_len = []
error_exit_flag = False
print('共有{}个标注文本'.format(len(txts)))
for txt in txts:
    print(lann_dir+txt)
    with open(lann_dir+txt,'r',encoding = 'utf8') as f:
        tokens_tmp = []
        labels_tmp = []
        spos_tmp = []
        content = f.read().splitlines()
        tmp = []
        tmpl = []
        last_label = "-1"
        location = 0
        for i,sample in enumerate(content):
            if sample.strip() == "":
                continue
            c,l,spo = sample.split('\t')
            tokens_tmp.append(c)
            tmp.append(c)
            if l[0] == 'I':
                if  last_label[0] == 'O' or l[2:] != last_label[2:]:
                    print('标签连续性错误：')
                    print(txt,i,last_label,c,l)
                    error_exit_flag = True
            if l not in labels:
                labels.append(l)
            statitic.append(l)
            if l[0] == 'B':
                entity_count += 1
            labels_tmp.append(l)
            tmpl.append(l)
            last_label = l
            last_token = c
            if c == '_换行符_' or c == '。':# 语料切分规则
                datas.append((tmp,tmpl,[txt,location]))
                char_len.append(len(tmp))
                tmp = []
                tmpl = []
                location = i+1
        if len(tmp)>10 :# 语料末尾没有“。”或者“_换行符_” 
                datas.append((tmp,tmpl,[txt,location]))
                char_len.append(len(tmp))
                tmp = []
                tmpl = []
        if error_exit_flag:
            import sys;sys.exit(0)
        chars_count += i
shuffle(datas)
cut_index = int(0.75*len(datas))
train_dataset = datas[:cut_index]
test_dataset = datas[cut_index:]
with open(result+'datas.txt','w',encoding = 'utf8') as f:
    f.write(str(datas))
with open(result+'train_datas.txt','w',encoding = 'utf8') as f:
    f.write(str(train_dataset))
with open(result+'test_datas.txt','w',encoding = 'utf8') as f:
    f.write(str(test_dataset))
with open(result+'labels.txt','w',encoding = 'utf8') as f:
    f.write(str(sorted(labels)))
char_len_test = [len(l[0]) for l in test_dataset]
char_len_train = [len(l[0]) for l in train_dataset]
print('{}个训练样本；{}个测试样本'.format(len(train_dataset),len(test_dataset)))
print('{}个训练字符；{}个测试字符'.format(int(0.75*chars_count),int(0.25*chars_count)))
print('{}个训练实体；{}个测试实体'.format(int(0.75*entity_count),int(0.25*entity_count)))
print('样本平均字符长度：{}\t最大长度：{}\t最小长度：{}'.format(mean(char_len),max(char_len),min(char_len)))
print('训练集样本 平均字符长度：{}\t最大长度：{}\t最小长度：{}'.format(mean(char_len_train),max(char_len_train),min(char_len_train)))
print('测试集样本 平均字符长度：{}\t最大长度：{}\t最小长度：{}'.format(mean(char_len_test),max(char_len_test),min(char_len_test)))
print('{}维标签样本'.format(len(labels)))
for c in list(set(statitic)):
    print('{}:{}'.format(c,statitic.count(c)))
print('提示：如果保留\'_换行符_\'，需要在模型字典中添加')
