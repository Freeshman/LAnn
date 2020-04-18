from django.http import HttpResponse
from django.http import JsonResponse
import torch.optim as optim
import torch
import torch.nn as nn
import torch.nn.functional as F
import time
#构建字典
class object2id():
    def __init__(self,vocb_file,label_file):
        self.char_diction=[]
        self.label_diction=[]
        self.vocb_file=vocb_file
        self.label_file=label_file
        self.read_vocb_file()
        self.read_label_file()
    def read_vocb_file(self):
        content=open(self.vocb_file,'r').read().splitlines()
        for i,c in enumerate(content):
            if c=='__换行符__':
                c='\n'
            self.char_diction.append(c)
        print('字符共{}维'.format(len(self.char_diction)))
    def char_get_id(self,char):
        if char in self.char_diction:
            return self.char_diction.index(char)
        else:
            return self.char_diction.index('[UNK]')
    def label_get_id(self,label):
        if label in self.label_diction:
            return torch.tensor([self.label_diction.index(label)])
        else:
            return torch.tensor([self.label_diction.index('OTH')])
    def sent_get_id(self,sent):
        idx=[]
        for c in sent:
            idx.append(self.char_get_id(c))
        return torch.tensor(idx)
    def id_get_char(self,i):
        if i<len(self.char_diction):
            return self.char_diction[i]
        else:
            return 'Out Of Vocabulary'
    def id_get_label(self,i):
        if i<len(self.label_diction):
            return self.label_diction[i]
        else:
            return 'Out Of Label'
    def ids_get_sent(self,ids):
        sent=''
        for i in ids:
            sent+=self.id_get_char(i)
        return sent
    def read_label_file(self):
        self.label_diction=eval(open(self.label_file,'r').read())
        print('标签共{}维'.format(len(self.label_diction)))
    def get_len(self,obj):
        if obj.upper()=='CHAR':
            return len(self.char_diction)
        elif obj.upper()=='LABEL':
            return len(self.label_diction)
    def get_label(self):
        print(self.label_diction)
class LAnn_prediction(nn.Module):
    def __init__(self,diction_size,embedding_dim,hidden_size,target_size):
        super(LAnn_prediction,self).__init__()
        self.input=nn.Embedding(diction_size,embedding_dim)
        self.gru=nn.GRU(embedding_dim,hidden_size,2,bidirectional=True,batch_first=True)
        self.ff=nn.ModuleList([nn.Linear(hidden_size,hidden_size) for i in range(5)])
        self.h2target=nn.Linear(hidden_size,target_size)
        self.activation=nn.SELU()
    def forward(self,data):
        data=self.input(data)
        gru_out,hidden=self.gru(data)
        gru_out=hidden[0]
        for l in self.ff:
            gru_out=self.activation(l(gru_out))
        score=self.activation(self.h2target(gru_out))
        return score
class LAnn_Plus_prediction(nn.Module):
    def __init__(self,diction_size,embedding_dim,hidden_size,target_size):
        super(LAnn_Plus_prediction,self).__init__()
        self.Hidden_size=hidden_size
        self.input=nn.Embedding(diction_size,embedding_dim)
        self.label_emb=nn.Embedding(target_size,2*hidden_size)
        # self.projector=nn.Linear(2*hidden_size+50,target_size)
        self.gru=nn.GRU(embedding_dim,hidden_size,1,bidirectional=True,batch_first=True)
        self.grufinal=nn.GRU(4*embedding_dim,hidden_size,1,bidirectional=True,batch_first=True)
        # self.h2h=nn.Linear(2*hidden_size,2*hidden_size)
        # self.h2target=nn.Linear(2*hidden_size,target_size)
        # self.activation=nn.SELU()
    def forward(self,data,length):
        embedded=self.input(data)
        packed = nn.utils.rnn.pack_padded_sequence(embedded, length, batch_first=True)
        gru_out,hidden=self.gru(packed)
        pad_output,l=nn.utils.rnn.pad_packed_sequence(gru_out,batch_first=True)

#         print((hidden[0]))
#         print(gru_out.size())
#         pad_output,l=nn.utils.rnn.pad_packed_sequence(gru_out,batch_first=True)
        q=pad_output
        k=self.label_emb.weight
        k=k.expand(q.size(0),k.size(0),k.size(1))
        v=k
        k_trans=k.transpose(2,1)
        # print(q.size(),k_trans.size())
        scaling_factor=torch.sqrt(torch.tensor(self.Hidden_size).float())
        Hl=torch.bmm(torch.softmax(torch.bmm(q,k_trans)/scaling_factor,-1),v)
        Hl=torch.cat([pad_output,Hl],2)
        # # print(Hl.size())

        Hfinal,hidden=self.grufinal(Hl)
        q=Hfinal
        k=self.label_emb.weight
        k=k.expand(q.size(0),k.size(0),k.size(1))
        v=k
        k_trans=k.transpose(2,1)
        # print(q.size(),k_trans.size())
        #scaling_factor=torch.sqrt(torch.tensor(self.Hidden_size).float())
        Hl=torch.bmm(q,k_trans)/scaling_factor
        # Hfinal=self.activation(F.dropout(self.h2h(Hfinal),0.1))
        # score=self.h2target(Hl)
        # score=self.activation(self.h2target(Hfinal))
        return Hl
things2id=object2id('vocab.txt','labels.txt')
things2id_seqlab=object2id('vocab.txt','labels_seqlab.txt')


model_seqlab=LAnn_Plus_prediction(things2id_seqlab.get_len('char'),128,128,things2id_seqlab.get_len('label'))

model_seqlab.load_state_dict(torch.load('LAnn_seqlab.pth',map_location='cpu')['state'])

model=LAnn_prediction(things2id.get_len('char'),128,128,things2id.get_len('label'))
model.load_state_dict(torch.load('LAnn_classfyer_state.pth',map_location='cpu')['state'])
new_training_sample=[]

# model=torch.load('LAnn_Back.pth')
print(model)
print(model_seqlab)
def GUI(request):
    return HttpResponse('Hello world!')
def seqlab(request):
    try:
        sample=request.POST['sample']
    except:
        return HttpResponse(JsonResponse({"status": '服务器接收失败'}))
    # print(sample)
    current_x=things2id.sent_get_id(sample)
    probability,prediction=torch.max(torch.softmax(model_seqlab(current_x.unsqueeze(0),[len(current_x)]),2),2)
    # print(prediction.squeeze(0).view(-1).size())
    labels=list(map(things2id_seqlab.id_get_label,prediction.view(-1).tolist()))
    # print(labels)
    for i in range(len(labels)-1):
        if labels[i][0]=="O" and labels[i+1][0]=="I":
            # print('======= {} ======='.format(i))
            # print(labels[i])
            # print(labels[i+1])
            labels[i+1]="O"
            # print(labels[i])
            # print(labels[i+1])
    # print(labels)

    data = {
        '预测值': labels,
        '可信度': probability.view(-1).tolist(),
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
    #prediction,probability=model(sample)
    print(request.POST)
    if request.POST['label']=='-1':
        current_x=things2id.sent_get_id(sample)
        probability,prediction=torch.max(torch.softmax(model(current_x.unsqueeze(0)),1),1)
        data = {
            '预测值': things2id.id_get_label(prediction.item()),
            '可信度': probability.item(),
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
# if request.method=="OPTIONS":
# #可以加*
#   print('Options')
#   response["Access-Control-Allow-Headers"]="Content-Type"
#   response["Access-Control-Allow-Origin"] = "*"
#   return response
