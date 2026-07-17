// Welcome Message

const username = document.querySelector("#username");

if(username){

    const hour = new Date().getHours();

    let greet = "";

    if(hour < 12)
        greet = "Good Morning";

    else if(hour < 18)
        greet = "Good Afternoon";

    else
        greet = "Good Evening";

    username.innerHTML = `${greet}, ${username.innerHTML}`;

}


// Live Date & Time

const clock = document.querySelector("#clock");

function updateClock(){

    const now = new Date();

    clock.innerHTML = now.toLocaleString();

}

updateClock();

setInterval(updateClock,1000);


// Logout Confirmation

const logout = document.querySelector(".logout-btn");

logout.addEventListener("click",function(e){

    const confirmLogout = confirm("Are you sure you want to logout?");

    if(!confirmLogout){

        e.preventDefault();

    }

});


// Dashboard Cards Animation

const cards = document.querySelectorAll(".card");

cards.forEach((card,index)=>{

    card.style.opacity="0";

    card.style.transform="translateY(20px)";

    setTimeout(()=>{

        card.style.transition="0.5s";

        card.style.opacity="1";

        card.style.transform="translateY(0)";

    },index*150);

});


// Authentication Status

const status = document.querySelector("#authStatus");

if(status){

    status.style.color="#22c55e";

    status.innerHTML="🟢 User Authenticated";

}