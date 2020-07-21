document.addEventListener('DOMContentLoaded', () => {

var socket=io.connect(location.protocol+'//'+document.domain+':'+location.port);
    socket.on('connect', async ()=>{
    console.log('connected!!!!!')
    var current_user=await load_name()
    var data=await get_messages()
    for(var i=0;i<data.data.length;i++){
        var username=data.data[i].username
        var message=data.data[i].message
        if (current_user===username){
                    add_messageonright(username,message)
        }
        else{
            add_messageonleft(username,message)
            }
    }
    document.querySelector('#msgForm').addEventListener('submit',async (e)=>{
    console.log('clicked')
    e.preventDefault();
    msg=document.querySelector('#msg').value;
    add_messageonright(current_user,msg);
    socket.emit('send_message',{name:current_user,msg:msg});
    })});

socket.on('receive',(data)=>{
    name=data.name;
    msg=data.msg;
    console.log('message received:'+ msg)
    add_messageonleft(name,msg)});



async function load_name(){
   return await fetch('/get_name').then(async (res)=> {return await res.json()})
    .then((data)=>{
    console.log(data.name)
    return data.name}).catch((err)=> console.log(err))}

async function get_messages(){
   return await fetch('/get_messages').then(async (res)=> {return await res.json()})
    .then(async (data)=>{
       return data
    }).catch((err)=> console.log(err))}


//name:load_name(),message:msg})
/*
document.querySelector('#sendBtn').onsubmit= (e)=>{
    console.log('clicked')
    e.preventDefault();
    msg=document.querySelector('#msg').value;
    add_message(message=msg);

async function load_name(){
    const request = new XMLHttpRequest();
     request.open('GET', '/get_name',true);
     request.onload = async () => {
     const data = JSON.parse(request.responseText);
            if(request.status===200){
            console.log(data.name)
            return data.name
            }
            else{
            console.log('couldn\'nt get the data from the server')}
            return 'couldn\'nt get the data from the server'
            }
            await request.send()
             }
*/
function dateNow() {
  var date = new Date();
  var year = date.getFullYear();
  var day = date.getDate();
  var month = (date.getMonth() + 1);
  var cur_day = day + "-" + month + "-" + year;

  var hours = date.getHours()
  var minutes = date.getMinutes()
  var seconds = date.getSeconds();

  if (hours < 10)
      hours = "0" + hours;

  if (minutes < 10)
      minutes = "0" + minutes;

  if (seconds < 10)
      seconds = "0" + seconds;

  return cur_day + " " + hours + ":" + minutes;
}


async function add_messageonleft(name,message){
    time=dateNow()
    if (message!==''){
      var  content = '<div class="container darker">' + '<b style="color:#000" class="left">'+name+'</b><p>' + message +'</p><span class="time-left">' + time + '</span></div>';
       var messageDiv = document.querySelector('#messages');
    messageDiv.innerHTML += content;
    document.querySelector('#msg').value=''
    scrollToBottom('messages')

  //document.querySelector('#messsages').srollTo()


 }}

async function add_messageonright(name,message){
 time=dateNow()
     if (message!==''){

     var content = '<div class="container">' + '<b style="color:#000" class="right">'+name+'</b><p>' + message +'</p><span class="time-right">' + time + '</span></div>';

    // update div
    var messageDiv = document.querySelector('#messages');
    messageDiv.innerHTML += content;
    document.querySelector('#msg').value=''
    //document.querySelector('#messsages').scrollTop=document.querySelector('#messages').offsetTop;
    scrollToBottom('messages')


}
 }
function scrollToBottom (id) {
   var div = document.getElementById(id);
   div.scrollTop = div.scrollHeight - div.clientHeight;
}


    })