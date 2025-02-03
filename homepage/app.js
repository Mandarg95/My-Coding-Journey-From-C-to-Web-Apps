var darkMode = document.querySelector('#switch-dw');
var body = document.querySelector('body');
var footer = document.querySelector('footer');
var count = 0;
darkMode.addEventListener('click',function(){
    if(count == 0){
        body.style.backgroundColor = "black";
        footer.style.backgroundColor = "white";
        body.style.color ="white";
        footer.style.color ="black";
        darkMode.innerHTML = "Light Mode"
        count = 1
    }else{
        body.style.backgroundColor = "white";
        footer.style.backgroundColor = "black";
        body.style.color ="black";
        footer.style.color ="white";
        darkMode.innerHTML = "Dark Mode"
        count = 0
    }
})
