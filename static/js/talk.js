var left =document.querySelector('.left');
var txt = document.querySelector('.txt');
var send = document.querySelector('.send');
var list = document.getElementById('list');

var user=1

left.onclick = function(){
    if(user==1){
        left.src ="../static/images/picture2.jpg";
        user=2;
    }else {
        left.src="../static/images/picture1.jpg";
        user=1;
    }
}

send.onclick = function(){
    if(txt.value){
        if(user==1){
            list.innerHTML+='<li class="clearfixd"><div class="text1 fl">' + txt.value + '</div><img class="imag1 fl" src="../static/images/picture1.jpg"></img></li>'
            txt.value='';
        }else{
            list.innerHTML+='<li class="clearfixd"></div><img class="imag1 fl" src="../static/images/picture2.jpg"></img><div class="text1 fl">' + txt.value + '</div></li>'
            txt.value='';
        }
    }
}