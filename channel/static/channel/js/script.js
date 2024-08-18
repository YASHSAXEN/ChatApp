var user = document.querySelector('.user');
var dashboard = document.querySelector('.dashcontainer');
var statusval = true;
dashboard.style.display = 'none';

user.addEventListener('click',()=>{
    console.log(statusval)
    if(statusval){
        dashboard.style.display = 'flex';
        statusval = false;
    }
    else{
        dashboard.style.display = 'none';
        statusval = true;
    }
})



