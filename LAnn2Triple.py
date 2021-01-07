#!/usr/bin/python
#coding=utf8
"""
# Author: hu-tom
# Created Time : 2020-02-24 18:46:36

# File Name: LAn2Triple.py
# Description:

"""
import os
import sys
from pylab import *
result='result/'
if not os.path.isdir(result):
    os.mkdir(result)
fs=os.listdir()
txts=[i for i in fs if i[-5:]=='.lann']
datas=[]
labels=[]
count=0
triple_all_count = 0
datas=[]
relation_labels=[]
entity_type=[]
relation2delete = [
    'list中添加临时跳过的关系',
]
skiped_count = 0
relation2delete = ['关系_'+l for l in relation2delete]
def find_end_and_type(start,labels):
    assert start+1 < len(labels),f'{start+1},{len(labels)}'
    for i,l in enumerate(labels[start+1:]):
        # print(tokens[start+i],labels[start],l)
        if l[0] in ['B','O']:
            return start+i,labels[start][2:]
def find_token_start(start,tokens):
    for i,t in enumerate(tokens[start::-1]):
        if t in ['。','_换行符_']:
            return start-i+1
    return 0
def find_token_end(start,tokens):
    for i,t in enumerate(tokens[start:]):
        if t in ['。','_换行符_']:
            return start+i+1
for txt in txts:
    # labels.append(txt[:-4])
    with open(txt,'r',encoding='utf8') as f:
        print(txt)
        datas_tmp={}
        tokens=[]
        labels=[]
        spos_all=[]
        spos_with_range=[]
        content=f.read().splitlines()
        count_tmp=0
        for i,sample in enumerate(content):
            if sample.strip()=="":
                continue
            c,l,spo=sample.split('\t')
            tokens.append(c)
            labels.append(l)
            if spo=='X':
                continue
            if ';' in spo:
                sposs=spo.split(';')
                triple_all_count += len(sposs)
                for spos in sposs:
                    if spos.split('>')[1] in relation2delete:
                        skiped_count +=1
                        continue
                    spos_all.append(spos)
                    count_tmp+=1
            else:
                triple_all_count += 1
                if spo.split('>')[1] in relation2delete:
                    skiped_count +=1
                    continue
                spos_all.append(spo)
                count_tmp+=1
        for spo in spos_all:
            # print(f'============ {spo} ===============')
            s,p,o=spo.split('>')
            es,ts=find_end_and_type(int(s),labels)
            if tokens[es] in [' ','_换行符_','。','.']:
                print('?',txt,es,tokens[es])
                print('该处实体结束位置可能不正确！')
            eo,to=find_end_and_type(int(o),labels)
            if tokens[eo] in [' ','_换行符_','。','.']:
                print('?',txt,eo,tokens[eo])
                print('该处实体结束位置可能不正确！')
            if p[0]!='关':
                try:
                    p=labels[int(p)][2:]
                except:
                    print(txt,spo)
                    import sys;sys.exit(0)
            # print(p)
            if p not in relation_labels:
                relation_labels.append(p)
            if ts not in entity_type:
                entity_type.append(ts)
            if to not in entity_type:
                entity_type.append(to)
            if '' in entity_type:
                print('Error !')
                print(txt,spo,'序列标注存在问题：类型为空白！')
                sys.exit(0)
            lb=min(int(s),int(o))
            ub=max(es,eo)
            tokens_start=find_token_start(lb,tokens)
            tokens_end=find_token_end(ub,tokens)
            flag=False
            # print(spo,lb,ub,tokens_start,tokens_end)
            if len(list(datas_tmp.keys()))>0:
                # print('list(datas_tmp.keys())={}'.format((list(datas_tmp.keys()))))
                for k in datas_tmp.keys():
                    assert 'location' in list(datas_tmp[k].keys()),f'No location {k},{txt},{list(datas_tmp.keys())}'
                    # print(datas_tmp[k])
                    if tokens_start>=k[0] and tokens_end<=k[1]:#新token范围更小  
                        # print('='*40)
                        # print('新token范围更小')              
                        # print(tokens_start,tokens_end)
                        # print(k)
                        datas_tmp[k]['spo_list'].append((''.join(tokens[int(s):es+1]),p,''.join(tokens[int(o):eo+1])))
                        datas_tmp[k]['spo_details'].append([int(s),es,ts,p,int(o),eo,to])
                        flag=True
                        break
                    elif tokens_start<=k[0] and tokens_end>=k[1]:#新token范围更大
                        # print('='*40)
                        # print('新token范围更大')              
                        # print(tokens_start,tokens_end)
                        # print(k)
                        datas_tmp[(tokens_start,tokens_end)]={}
                        datas_tmp[(tokens_start,tokens_end)]['tokens']=tokens[tokens_start:tokens_end]
                        datas_tmp[(tokens_start,tokens_end)]['spo_list']=datas_tmp[k]['spo_list']+[(''.join(tokens[int(s):es+1]),p,''.join(tokens[int(o):eo+1]))]
                        datas_tmp[(tokens_start,tokens_end)]['spo_details']=datas_tmp[k]['spo_details']+[[int(s),es,ts,p,int(o),eo,to]]
                        datas_tmp.pop(k)
                        datas_tmp[(tokens_start,tokens_end)]['location']= f'{txt}:{tokens_start}'
                        flag=True
                        break
                    elif tokens_start<=k[0] and tokens_end>k[0] and tokens_end<=k[1]:#新token左边范围更大，重复部分右范围
                        # print('='*40)
                        # print(tokens_start,tokens_end)
                        # print(k)
                        # print('新token左边范围更大，重复部分右范围') 
                        datas_tmp[(tokens_start,k[1])]['tokens']={}
                        datas_tmp[(tokens_start,k[1])]['tokens']=tokens[tokens_start:k[1]]
                        datas_tmp[(tokens_start,k[1])]['spo_list']=datas_tmp[k]['spo_list']+[(''.join(tokens[int(s):es+1]),p,''.join(tokens[int(o):eo+1]))]
                        datas_tmp[(tokens_start,k[1])]['spo_details']=datas_tmp[k]['spo_details']+[[int(s),es,ts,p,int(o),eo,to]]
                        datas_tmp.pop(k)
                        datas_tmp[(tokens_start,k[1])]['location']= f'{txt}:{tokens_start}'
                        flag=True
                        break

                    elif tokens_start>=k[0] and tokens_start<=k[1] and tokens_end>=k[1]:#新token右边范围更大，重复部分左范围
                        # print('='*40)
                        # print('新token右边范围更大，重复部分左范围') 
                        # print(tokens_start,tokens_end)
                        # print(k)
                        datas_tmp[(k[0],tokens_end)]={}
                        datas_tmp[(k[0],tokens_end)]['tokens']=tokens[k[0]:tokens_end]
                        datas_tmp[(k[0],tokens_end)]['spo_list']=datas_tmp[k]['spo_list']+[(''.join(tokens[int(s):es+1]),p,''.join(tokens[int(o):eo+1]))]
                        datas_tmp[(k[0],tokens_end)]['spo_details']=datas_tmp[k]['spo_details']+[[int(s),es,ts,p,int(o),eo,to]]
                        datas_tmp.pop(k)
                        datas_tmp[(k[0],tokens_end)]['location']= f'{txt}:{k[0]}'
                        flag=True
                        break
                    elif tokens_start>k[1] and k==list(datas_tmp.keys())[-1]:
                        # print('='*40)
                        # print('新范围的token') 
                        # print(tokens_start,tokens_end)
                        # print(k)
                        datas_tmp[(tokens_start,tokens_end)]={'tokens':tokens[tokens_start:tokens_end],'spo_list':[(''.join(tokens[int(s):es+1]),p,''.join(tokens[int(o):eo+1]))],'spo_details':[[int(s),es,ts,p,int(o),eo,to]]}
                        flag=True
                        datas_tmp[(tokens_start,tokens_end)]['location']= f'{txt}:{tokens_start}'
                        break
                # print('xxx'*30)
                # print('查找完毕')
            if not flag:#没找到之前合适的区间，新生成区间
                # print('n'*30)
                # print('没找到之前合适的区间，新生成区间')
                datas_tmp[(tokens_start,tokens_end)]={'tokens':tokens[tokens_start:tokens_end],'spo_list':[(''.join(tokens[int(s):es+1]),p,''.join(tokens[int(o):eo+1]))],'spo_details':[[int(s),es,ts,p,int(o),eo,to]]}
                datas_tmp[(tokens_start,tokens_end)]['location']= f'{txt}:{tokens_start}'
        if(len(datas_tmp.keys())==0):
            continue
        keys=list(datas_tmp.keys())
        for k in keys:
            for i,spos in enumerate(datas_tmp[k]['spo_details']):
                for j in [0,1,4,5]:
                    # print('-'*30)
                    # print(k[0])
                    # print(datas_tmp[k]['spo_details'][i][j])
                    datas_tmp[k]['spo_details'][i][j]-=k[0]
                    # print(datas_tmp[k]['spo_details'][i][j])
            
        vv = list(datas_tmp.values())#该语料文件所有起始区间对应的三元组数据
        for v in vv:#数据完整性检查
            # print(v)
            tokens_check = v['tokens']
            spo_list_check = v['spo_list']
            spo_detail_check = v['spo_details']
            for li,de in zip(spo_list_check,spo_detail_check):
                # print(li,de)
                e1 = li[0]
                e2 = li[2]
                se1 = de[0]
                ee1 = de[1]
                se2 = de[4]
                ee2 = de[5]
                # print(se1,ee1,se2,ee2,len(tokens_check))
                # print(tokens_check[se1],tokens_check[ee1],tokens_check[se2],tokens_check[ee2])
                c1 =  tokens_check[se1]==e1[0] and \
                    tokens_check[ee1]==e1[-1] and \
                    tokens_check[se2]==e2[0] and \
                    tokens_check[ee2]==e2[-1]
                assert c1==True,f"Error!!!!{v}{v['location']}"
    
        datas+=list(datas_tmp.values())
        count+=count_tmp
shuffle(datas)
def statistic(datas):
    print('='*40)
    statistic_result = {}
    spo_count = 0
    seq_len = 0
    for d in datas:
        spo_list = d['spo_list']
        seq_len += len(d['tokens'])
        spo_count += len(spo_list)
        for spo in spo_list:
            relation = spo[1][3:]
            if relation not in statistic_result:
                statistic_result[relation] = 0
            statistic_result[relation] += 1
    for k,v in statistic_result.items():
        print('\t',k,v)
    print(f'\t共有{spo_count}个三元组')
    print(f'\t平均长度:{seq_len/spo_count}')

cut_index = int(0.75*len(datas))
train_datas = datas[0:cut_index]
test_datas = datas[cut_index:]
statistic(train_datas)
statistic(test_datas)
print('='*40)
print('数据集整体信息:')
print('\t共{}个三元组'.format(triple_all_count))
print('\t剩下{}个三元组'.format(count))
print('\t去掉{}个三元组'.format(skiped_count))
print('\t共{}个样本'.format(len(datas)))
print(f'\t共{len(train_datas)}个训练样本，共{len(test_datas)}个测试样本')
print(f'\t共{len(entity_type)}个实体类型：{entity_type}')
print(f'\t共{len(relation_labels)}个关系类型：{relation_labels}')
relation_labels = sorted(relation_labels)
entity_type = sorted(entity_type)
with open('result/datasets.txt','w',encoding='utf8') as f:
    f.write(str(datas))
with open(result+'train_datas.txt','w',encoding='utf8') as f:
    f.write(str(train_datas))
with open(result+'test_datas.txt','w',encoding='utf8') as f:
    f.write(str(test_datas))
with open(result+'relation_labels.txt','w',encoding='utf8') as f:
    f.write(str(relation_labels))
with open(result+'entity_type.txt','w',encoding='utf8') as f:
    f.write(str(entity_type))
