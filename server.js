function cut_sample(start_end){
    // var left_flag=true;
    // var right_flag=true;
    // var index_left=0;
    // for(var i=0;i<length;i++){
    //     index
    // }
    // return 
}
function to_server(server_usable,sample){
    // if(!server_usable)return;
    console.log(sample);
    $.ajax({
  url:'http://127.0.0.1:8000/pr/',//目的php文件
  data:{"sample":sample},//传输的数据
  type:'post',//数据传送的方式get/post
  // type:'get',//数据传送的方式get/post
  scriptCharset: 'utf-8',
  dataType:'json',//数据传输的格式是json
  success:function(response){
    //数据给后端php文件并成功返回
    console.log(response['result']);//打印返回的值
    // init_entities_list=eval(response);
  }
})
}