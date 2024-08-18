let menubar = document.querySelector('.menubar');
let detailscontaincontainer = document.querySelector('.detailscontaincontainer');
let cancelbutton = document.querySelector('.cancelbutton');

menubar.addEventListener('click',()=>{
    detailscontaincontainer.style.top = '0px';
})

cancelbutton.addEventListener('click',()=>{
    detailscontaincontainer.style.top = '-1000px';
})