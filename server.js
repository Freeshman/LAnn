function server_triple_relation_classfy_django(triple_relation_classfy_list,label,add_delete){
//  console.log(seqlab_flag,sample);//dev
  $.ajax({
        url:'http://255.255.255.255/triple_relation_classfy/',//目的php文件
        // data:{"e1":e1,"e1_index":e1_index,"e2":e2,"e2_index":e2_index,"tokens":tokens},//传输的数据
        data:{"sample":triple_relation_classfy_list,'label':label,'add_delete':add_delete},//传输的数据
        type:'post',//数据传送的方式get/post
        // type:'get',//数据传送的方式get/post
        scriptCharset: 'utf-8',
        dataType:'json',//数据传输的格式是json
        success:function(response){
          //数据给后端php文件并成功返回
          // console.log(response);//打印返回的值 //dev
          if(add_delete=='query'){
                //query:查询模式，服务器预测；
                //add:  添加模式，直接上传到服务器上去；
                //delete：删除模式，删除指定的三元组相关数据。
                type_choose(false,response['result']);//服务器预测类别后进入选择窗口；如果添加新样本，不显示选择窗口
                // console.log('server.js 打开type_choose');
                // type_choose(false,{"预测值":"服务器不可用","可信度":"0"});

              }
            // set_labels(response['result']);
        },
        error:function(xhr,state,errorThrown){
          // myconsole('server.js',add_delete);//dev
          var tp = triple_relation_classfy_list;
          var triple_relation_classfy_list_tmp = ['#',tp[0],tp[1],tp[4],tp[5],tp[8].join('')];
          if(add_delete=='query'){
            var relation_label_local = '服务器不可用';
            var probability = 0;
            if(Object.keys(relation_diction).length>1){
              var tmp = relation_classfy_local(triple_relation_classfy_list,relation_diction);
              relation_label_local = tmp[0];
              probability = tmp[1];
            }
            type_choose(false,{"预测值":relation_label_local,"可信度":probability});
          }else if(add_delete=='add'){
              // myconsole('从字典中添加'+label);//dev
              relation_diction[triple_relation_classfy_list_tmp.join('  ')] = label;
          }else if(add_delete=='delete'){
              // myconsole('从字典中删除'+label);//dev
              var tmp = triple_relation_classfy_list_tmp.join('  ');
              if(tmp in relation_diction)delete relation_diction[tmp];
            } 
        }
})
}
function seq_labing_to_server_django(seqlab_flag,sample,add_delete){
//  console.log(seqlab_flag,sample);//dev
  if(!seqlab_flag)return;
  $.ajax({
        url:'http://255.255.255.255/seqlab/',//目的php文件
        data:{"sample":sample},//传输的数据
        type:'post',//数据传送的方式get/post
        // type:'get',//数据传送的方式get/post
        scriptCharset: 'utf-8',
        dataType:'json',//数据传输的格式是json
        success:function(response){
        //数据给后端php文件并成功返回
         console.log(response);//打印返回的值 //dev
          set_labels(response['result']);
        },
        error:function(xhr,state,errorThrown){
                // requesFail(xhr);
                myconsole('传统方法进行标注！',add_delete);//dev
                if(add_delete=='query'){
                  var sample_tmp = []
                  if(Object.keys(entity_diction).length>0){
                    for(var i in sample){
                      if(sample[i]=='_换行符_')sample_tmp.push('\n');
                      else sample_tmp.push(sample[i]);
                    }
                    sample_tmp = sample_tmp.join('');
                    seq_label_local(sample_tmp,entity_diction);
                  }
                }
        			}
})
}
function to_server_django(entity,sample,index_s,index_e,tokens,label,add_delete){
//    console.log(sample,label); //dev
    $.ajax({
          url:'http://255.255.255.255/pr/',//目的php文件
          data:{"sample":sample,"index_s":index_s,"index_e":index_e,"tokens":tokens,"label":label,'add_delete':add_delete},//传输的数据
          type:'post',//数据传送的方式get/post
          // type:'get',//数据传送的方式get/post
          scriptCharset: 'utf-8',
          dataType:'json',//数据传输的格式是json
          success:function(response){
          //数据给后端php文件并成功返回
          //    console.log(response);//打印返回的值 //dev
          //实体类型选择
            if(add_delete=='query'){
              type_choose(entity,response['result']);//服务器预测类别后进入选择窗口；如果添加新样本，不显示选择窗口
            }
            // return response['result'];

            // init_entities_list=eval(response);
          },
          error:function(xhr,state,errorThrown){
            // myconsole('server.js',add_delete,sample,label);//dev
            var probability = 0;
            var label_predicted_local = "服务器不可用";
            if(add_delete=='query'){
              if(Object.keys(entity_diction).length>2){
                var tmp = entity_classfy_local(sample,entity_diction);
                label_predicted_local = tmp[0];
                probability = tmp[1];
              }
              // myconsole('label_predicted_local',label_predicted_local);
              type_choose(entity,{"预测值":label_predicted_local,"可信度":probability});
            }else if(add_delete=='delete'){
              if(sample in entity_diction) delete entity_diction[sample];
            }
          }
})
}
function entity_classfy_local(sample,entity_diction){
  var probability = 0;
  var label_predicted_local = "";
  if(sample in entity_diction){
    label_predicted_local = entity_diction[sample];
    probability = 1;
  }
  else
  {
    var min_distance = 999;
    for(var j in entity_diction){
      var distance = minDistance(j,sample);
      if(distance<min_distance){
        min_distance = distance;
        probability = 1-min_distance/Math.max(sample.length,j.length);
        label_predicted_local = entity_diction[j]
        if(probability>0.8)break;
      }
    } 
  }
  return [label_predicted_local,probability]
}
function relation_classfy_local(tp,relation_diction){
  var relation_label_local = '';
  var probability = 0;
  var triple_relation_classfy_list_tmp = ['#',tp[0],tp[1],tp[4],tp[5],tp[8].join('')].join('  ');
  var distance = 0;
  var min_distance = 999;
  // myconsole('triple_relation_classfy_list_tmp',triple_relation_classfy_list_tmp);//dev
  if(triple_relation_classfy_list_tmp in relation_diction) {
    relation_label_local = relation_diction[triple_relation_classfy_list_tmp];
    probability = 1;
  }else
  {
    var triple_relation_classfy_list_tmp = [tp[0],tp[1],tp[4],tp[5]];
    for(var description in relation_diction){
      var description_tmp = description.split('  ')
      description_tmp = description_tmp.slice(1,description_tmp.length-1);
      var distance = 0;
      var probability = 0
      var weight = [0.2,0.3,0.2,0.3];//实体类型的权重更大
      var distance_total = 0;
      for(var j in triple_relation_classfy_list_tmp){
        distance += weight[j]*minDistance(triple_relation_classfy_list_tmp[j],description_tmp[j]);
        distance_total+=Math.max(triple_relation_classfy_list_tmp[j].length,description_tmp[j].length);
      }
      probability = distance/distance_total;
      // console.log(probability,distance,min_distance);//dev
      if(distance<min_distance){
        min_distance = distance;
        relation_label_local = relation_diction[description]
        if(probability>0.8)break;
      }
    }
  }
  return [relation_label_local,probability];
}
function seq_label_local(sample_tmp,entity_diction){
  var list_tmp = Object.keys(entity_diction).sort(function(a,b){return b.length-a.length;});
  for(var ee in list_tmp){
    var entity = list_tmp[ee];
    // console.log('检查',entity);//dev
    var start_p = -1;
    var n = 510;
    while(n>0){
      n--;
      var target_p = sample_tmp.indexOf(entity,start_p+1);
      if(target_p==-1)break;
      else{
        // myconsole('标注',entity,start_p,target_p,entity_diction[entity],sample_tmp.slice(target_p,target_p+entity.length),entity.length);
        set_type_tradition(entity,entity_diction[entity],[target_p,target_p+entity.length-1]);
        start_p = target_p;
      }
    }
  }
  refresh();
}