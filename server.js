
function seq_labing_to_server(seqlab_flag,sample){
//  console.log(seqlab_flag,sample);//dev
  if(!seqlab_flag)return;
  $.ajax({
        url:'http://127.0.0.1:8000/seqlab/',//目的php文件
        data:{"sample":sample},//传输的数据
        type:'post',//数据传送的方式get/post
        // type:'get',//数据传送的方式get/post
        scriptCharset: 'utf-8',
        dataType:'json',//数据传输的格式是json
        success:function(response){
        //数据给后端php文件并成功返回
        //  console.log(response);//打印返回的值 //dev
          set_labels(response['result']);
        },
        error:function(xhr,state,errorThrown){
        				// requesFail(xhr);
        			}
})
}
function to_server(server_usable,entity,sample,label){
//    console.log(sample,label); //dev
    $.ajax({
          url:'http://127.0.0.1:8000/pr/',//目的php文件
          data:{"sample":sample,"label":label},//传输的数据
          type:'post',//数据传送的方式get/post
          // type:'get',//数据传送的方式get/post
          scriptCharset: 'utf-8',
          dataType:'json',//数据传输的格式是json
          success:function(response){
          //数据给后端php文件并成功返回
          //    console.log(response);//打印返回的值 //dev
          //实体类型选择
            if(label==-1){
              type_choose(entity,response['result']);//服务器预测类别后随机进入选择窗口；如果添加新样本，不显示选择窗口
            }
            // return response['result'];

            // init_entities_list=eval(response);
          },
          error:function(xhr,state,errorThrown){
              type_choose(entity,{"预测值":"服务器不可用","可信度":"0"});
          			}
})
}
