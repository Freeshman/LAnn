number_map = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9','a','b',
'c','d','e','f','g','h','i','j','k','l','m','n','o','p','k','r','s','t',
'u','v','w','x','y','z']
function keyboard_bind(){
  //    myconsole('绑定按键！');//dev
  //    Mousetrap.bind('space',function(){myconsole('空格');});//dev
       Mousetrap.bind('s', function() { add_entity(); });
       // Mousetrap.bind('f', function() { add_relation(); });
       Mousetrap.bind('f', function() {number_record('15'); });
       Mousetrap.bind('a', function() { cancle(); });
       Mousetrap.bind('h', function() { cursor_left(); });
       Mousetrap.bind('g', function() { cursor_left_twice(); });
       Mousetrap.bind('i', function() { number_record('18');  });
       Mousetrap.bind('l', function() { cursor_right(); });
       Mousetrap.bind(';', function() { cursor_right_twice(); });
       Mousetrap.bind('j', function() { cursor_down(); });
       Mousetrap.bind('k', function() { cursor_up(); });
       Mousetrap.bind('n', function() { next(true); });
       Mousetrap.bind('b', function() { previous(true); });
       Mousetrap.bind('c', function() { number_record('12'); });
       Mousetrap.bind('d', function() { number_record('13'); });
       Mousetrap.bind('e', function() { forward(); });
       Mousetrap.bind('r', function() { forward_end(); });
       Mousetrap.bind('w', function() { back(); });
       Mousetrap.bind('0', function() { number_record('0'); });
       Mousetrap.bind('1', function() { number_record('1'); });
       Mousetrap.bind('2', function() { number_record('2'); });
       Mousetrap.bind('3', function() { number_record('3'); });
       Mousetrap.bind('4', function() { number_record('4'); });
       Mousetrap.bind('5', function() { number_record('5'); });
       Mousetrap.bind('6', function() { number_record('6'); });
       Mousetrap.bind('7', function() { number_record('7'); });
       Mousetrap.bind('8', function() { number_record('8'); });
       Mousetrap.bind('9', function() { number_record('9'); });
       Mousetrap.bind('p', function() { keyboard_spo(); });
       Mousetrap.bind('u', function() { insert_char(); });
       Mousetrap.bind('enter', function() { jump(true); });
       Mousetrap.bind('esc', function() { number_record('clean'); });
       Mousetrap.bind('ctrl+g', function(){ jump_2_char_total_index();});
       Mousetrap.bind('ctrl+p', function(){ debug();});
       Mousetrap.bind('x', function(){ delete_char();});
       Mousetrap.bind('v', function() { selecte(); });
       Mousetrap.bind('space', function() { selecte(); });
       Mousetrap.bind('backspace', function() { backspace(); });    
  }