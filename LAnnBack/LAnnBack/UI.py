from django.http import HttpResponse
from django.http import JsonResponse
import time

new_training_sample=[]
new_training_sample_triple=[]
def GUI(request):
    return HttpResponse('Hello world!')
def seqlab(request):
    try:
        sample=request.POST['sample']
    except:
        return HttpResponse(JsonResponse({"status": '服务器接收失败'}))

    ### Modify Start
    labels ='序列标注结果'#model(sample)
    probability = 0.9#'实体_shiti 概率
    ### Modify End

    data = {
        '预测值': labels,
        '可信度': probability,
    }
    response = JsonResponse({"status": '服务器接收成功', 'result': data})
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Headers"] = "*"
    response["Access-Control-Allow-Headers"]="Content-Type"
    return HttpResponse(response)
def process(request):
    sample=request.POST['sample']
    add_delete=request.POST['add_delete']
    tokens=request.POST['tokens']
    index_s=int(request.POST['index_s'])
    index_e=int(request.POST['index_e'])
    if request.POST['label']=='-1':

        ### Modify Start
        class_predicted = '实体_shiti'#model(sample,tokens,index_s,index_e)
        probability = 0.9#'实体_shiti 概率
        ### Modify End

        data = {
            '预测值': class_predicted,
            '可信度': probability,
        }
    else:
        label=request.POST['label']
        data='{}'.format((sample,index_s,index_e,tokens,label))
        print(data in new_training_sample)
        if add_delete=='delete':
            if data in new_training_sample:
                new_training_sample.pop(new_training_sample.index(data))
                print('已删除:\n{}'.format(data))
            try:
                with open('new/entity_classfy/samples.txt','r') as f:
                    stored_sample=f.read().splitlines()
                    if data in stored_sample:
                        stored_sample.pop(stored_sample.index(data))
                        print('文件中已删除:\n{}'.format(data))
                with open('new/entity_classfy/samples.txt','w') as f:
                    f.write('\n'.join(stored_sample))
            except:
                pass
        else:
            if data not in new_training_sample:
                new_training_sample.append(data)
                print('已添加:\n{}'.format(data))
            flag=False
            with open('new/entity_classfy/samples.txt','a') as f:
                f.write('\n{}\n'.format(data))
                print('实体分类文件中已添加:\n{}'.format(data))
                flag=True
            data = {
                'received_len':len(sample) ,
                'total_new_len': len(new_training_sample),
                'stored_2_file':flag,
            }
    response = JsonResponse({"status": '服务器接收成功', 'result': data})
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Headers"] = "*"
    response["Access-Control-Allow-Headers"]="Content-Type"
    return HttpResponse(response)
def triple_relation_classfy(request):
    try:
        sample=request.POST.getlist('sample[]')
        add_delete=request.POST['add_delete']
    except:
        print('提取sample失败！')
        return HttpResponse(JsonResponse({"status": '服务器接收失败'}))
    if request.POST['label']=='-1':
        x=sample

        ### Modify Start
        relation_predicted = '关系_guanxi'#model(x)
        probability = 0.9#'关系_guanxi' 概率
        ### Modify End

        data = {
            '预测值': relation_predicted,
            '可信度': probability,
        }
    else:
        label=request.POST['label']
        data='({},\'{}\')'.format(sample,label)
        if add_delete=='delete':
            if data in new_training_sample_triple:
                new_training_sample_triple.pop(new_training_sample_triple.index(data))
                print('已删除{}：{}样本'.format(sample,label))
            with open('new/triple_relation_classfy/samples.txt','r') as f:
                stored_sample=f.read().splitlines()
                if data in stored_sample:
                    stored_sample.pop(stored_sample.index(data))
                    print('文件中已删除{}：{}样本'.format(sample,label))
            with open('new/triple_relation_classfy/samples.txt','w') as f:
                f.write('\n'.join(stored_sample))
        else:
            if data not in new_training_sample_triple:
                new_training_sample_triple.append(data)
                print('已添加{}：{}样本'.format(sample,label))
            flag=False
            with open('new/triple_relation_classfy/samples.txt','a') as f:
                f.write('\n{}\n'.format(data))
                print('三元组分类文件中已添加:\n{}'.format(data))
                flag=True
            data = {
                'received_len':len(sample) ,
                'total_new_len': len(new_training_sample_triple),
                'stored_2_file':flag,
            }
    response = JsonResponse({"status": '服务器接收成功', 'result': data})
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Headers"] = "*"
    response["Access-Control-Allow-Headers"]="Content-Type"
    return HttpResponse(response)