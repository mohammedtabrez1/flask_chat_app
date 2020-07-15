document.addEventListener('DOMContentLoaded', () => {

const request = new XMLHttpRequest();

var socket=io.connect(location.protocol+'//'+document.domain+':'+location.port);
    document.querySelector('#sendBtn').onsubmit =(e)=>{
    e.preventDefault();
    msg=document.querySelector('#msg').value;
    add_message(message=msg);
    socket.on('connect',()=>
    socket.emit('send_message',{name:load_name(),message:msg}))};


socket.on('receive',(data)=>{
    name=data[name];
    msg=data[msg];
    add_message(name,msg)});


function load_name(){
          request.open('GET', '/get_name');
          request.onload = () => {
              const data = JSON.parse(request.responseText);
               console.log(data);
          return data['name']}};


function add_message(name,message){{
    var content = '<div class="container">' + '<b style="color:#000" class="right">'+name+'</b><p>' + message +'</p><span class="time-right">' + n + '</span></div>'
    if (name == 'undefined'){
      name=load_name();
      content = '<div class="container darker">' + '<b style="color:#000" class="left">'+name+'</b><p>' + msg.message +'</p><span class="time-left">' + n + '</span></div>'
    }
    // update div
    var messageDiv = document.querySelector('#messages');
    messageDiv.innerHTML += content;
  }

  if (scroll){
    scrollSmoothToBottom('messages');
  }}

function scrollSmoothToBottom (id) {
   var div = document.getElementById(id);
   $('#' + id).animate({
      scrollTop: div.scrollHeight - div.clientHeight
   }, 500);

}

function scrollSmoothToBottom (id) {
   var div = document.getElementById(id);
   $('#' + id).animate({
      scrollTop: div.scrollHeight - div.clientHeight
   }, 500);
}
    })