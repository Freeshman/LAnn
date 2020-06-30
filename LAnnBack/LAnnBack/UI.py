from django.http import HttpResponse
from django.http import JsonResponse
import time

new_training_sample=[]
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
    try:
        sample=request.POST['sample']
    except:
        return HttpResponse(JsonResponse({"status": '服务器接收失败'}))
    if request.POST['label']=='-1':

        ### Modify Start
        class_predicted = '实体_shiti'#model(sample)
        probability = 0.9#实体_shiti 概率
        ### Modify End

        data = {
            '预测值': class_predicted,
            '可信度': probability,
        }
    else:
        label=request.POST['label']
        data='{}\t{}'.format(sample,label)
        if data not in new_training_sample:
            new_training_sample.append(data)
        with open('new/{}.txt'.format(label),'a') as f:
            f.write('{}\n'.format(sample))
        data = {
            'received_len':len(sample) ,
            'total_new_len': len(new_training_sample),
        }
    response = JsonResponse({"status": '服务器接收成功', 'result': data})
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Headers"] = "*"
    response["Access-Control-Allow-Headers"]="Content-Type"
    return HttpResponse(response)

