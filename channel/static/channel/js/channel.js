var groupname = document.querySelector('#groupnam');
var websocket = new WebSocket(`ws://${window.location.host}/ws/wsc/${groupname.innerHTML}`);
var button = document.querySelector('#button');
var chat_box = document.querySelector('.chat-box');
var close = document.querySelector('#logout-button');
var private = document.querySelector('#private');
var div_element = document.querySelectorAll('.actual-message');
var upload = document.querySelector('.upload');
var cancel = document.querySelector('.cancel');


var colors = ['#00ff00', '#ff3333', '#ffff00', '#ff6600']; 


for (let index = 0; index < div_element.length; index++) {
    const element = div_element[index];
    const random_color = colors[(Math.floor(Math.random() * colors.length))]; 
    element.style.backgroundColor = random_color;
}


websocket.addEventListener('open',(event)=>{
    setTimeout(()=>{
        scrolltobottom()
    },2000)
    
})

websocket.addEventListener('message',(event)=>{
    data = JSON.parse(event.data)
    if (data.status === 'new'){
        const para = document.createElement("div");
        const node1 = document.createElement('p');
        node1.innerText = `${data.user} joined the group `;
        node1.style.fontWeight = '900';
        node1.style.borderRadius ='10px';
        node1.style.fontFamily = 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', "Arial", "sans-serif";
        node1.style.padding ='10px';
        para.style.display = 'flex';
        node1.style.fontSize ='12px';
        para.style.justifyContent ='center';
        para.style.width='90%';
        para.appendChild(node1);
        chat_box.appendChild(para);
        var count = document.querySelector('#count');
        count.innerHTML = data.ct;
        setTimeout(()=>{
            scrolltobottom()
        },2000)
    }
    else if(data.status ==='close'){
        const para = document.createElement("div");
        const node1 = document.createElement('p');
        node1.innerText = `${data.user} leave the group `;
        node1.style.fontWeight = '900';
        node1.style.fontFamily = 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', "Arial", "sans-serif";
        node1.style.padding ='10px';
        node1.style.borderRadius ='10px';
        node1.style.fontSize ='12px';
        para.style.display = 'flex';
        para.style.justifyContent ='center';
        para.style.width='90%';
        para.appendChild(node1);
        chat_box.appendChild(para);
        var count = document.querySelector('#count');
        count.innerHTML = data.ct;
        scrolltobottom()
    }
    else if(data.status === "change"){
        var count = document.querySelector('#count');
        count.innerHTML = data.ct;
    }
    else if(data.status ==='private'){
        const value = data.value;
        if (value === "true"){
            const para = document.createElement("div");
            const node1 = document.createElement('p');
            node1.innerText = `Group is Private now`;
            node1.style.fontWeight = '900';
            node1.style.borderRadius ='10px';
            node1.style.fontFamily = 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', "Arial", "sans-serif";
            node1.style.padding ='10px';
            para.style.display = 'flex';
            node1.style.fontSize ='12px';
            para.style.justifyContent ='center';
            para.style.width='90%';
            para.appendChild(node1);
            chat_box.appendChild(para);
            document.querySelector('#private').checked = true;
            scrolltobottom()
        }
        else{
            const para = document.createElement("div");
            const node1 = document.createElement('p');
            node1.innerText = `Group is Public now`;
            node1.style.fontWeight = '900';
            node1.style.borderRadius ='10px';
            node1.style.fontFamily = 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', "Arial", "sans-serif";
            node1.style.padding ='10px';
            para.style.display = 'flex';
            node1.style.fontSize ='12px';
            para.style.justifyContent ='center';
            para.style.width='90%';
            para.appendChild(node1);
            chat_box.appendChild(para);
            document.querySelector('#private').checked = false;
            scrolltobottom()
        }
    }
    else if(data.status ==='image-uploaded-done'){
        const random_color = colors[(Math.floor( Math.random() * colors.length))]; 
        const para = document.createElement("div");
        para.classList.add('message-div');
        const node1 = document.createElement('p');
        node1.innerText = `${data.user}: `;
        const node2 = document.createElement('p');
        node2.classList.add('actual-message');
        const node3 = document.createElement('img');
        node3.style.width ='100%';
        node3.style.height ='100%';
        node3.src = data.url;
        node2.style.backgroundColor = random_color;
        node2.appendChild(node3);
        para.appendChild(node1);
        para.appendChild(node2);
        chat_box.appendChild(para);
        scrolltobottom()
    }
    else{
        const random_color = colors[(Math.floor( Math.random() * colors.length))]; 
        const para = document.createElement("div");
        para.classList.add('message-div');
        const node1 = document.createElement('p');
        const span = document.createElement('span');
        span.innerText =  ` (${data.time}):`
        span.style.fontSize ='12px';
        span.style.fontWeight ='bold';
        node1.innerText = `${data.user}`;
        const node2 = document.createElement('p');
        node2.classList.add('actual-message');
        node2.textContent = data.message;
        node2.style.backgroundColor = random_color;
        node1.appendChild(span);
        para.appendChild(node1);
        para.appendChild(node2);
        chat_box.appendChild(para);
        scrolltobottom()
    }
})

button.addEventListener('click',()=>{
    console.log('button clicked');
    var message = document.querySelector('#message');
    var message_content = message.value;
    console.log(message_content)
    if (message_content !==""){
        websocket.send(message_content)
    }
    message.value = '';
})

close.addEventListener('click',()=>{
    websocket.send('close');
})

private.addEventListener('click',()=>{
    const privated = document.querySelector('#private');
    const valued = privated.checked;
    if (valued === true){
        websocket.send("private_false");
    }
    else{
        websocket.send("public_true");
    }
})

function scrolltobottom(){
    chat_box.scrollTop = chat_box.scrollHeight;
}

upload.addEventListener('click',()=>{
   document.querySelector('.file-upload-container').style.display = 'flex';
   document.querySelector('.normal1').classList.add('hide-class');
   document.querySelector('.normal2').classList.add('hide-class');
})

cancel.addEventListener('click',()=>{
   document.querySelector('.file-upload-container').style.display = 'none';
   document.querySelector('.normal1').classList.remove('hide-class');
   document.querySelector('.normal2').classList.remove('hide-class');
})