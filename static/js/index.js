// Navbar active link

const links = document.querySelectorAll(".nav-links a");

links.forEach(link => {

    link.addEventListener("click", function(){

        links.forEach(l => l.classList.remove("active"));

        this.classList.add("active");

    });

});


// Smooth Scroll

document.querySelectorAll('a[href^="#"]').forEach(anchor => {

    anchor.addEventListener("click", function(e){

        e.preventDefault();

        document.querySelector(this.getAttribute("href"))
        .scrollIntoView({
            behavior: "smooth"
        });

    });

});


// Fade animation while scrolling

const cards = document.querySelectorAll(".card, .tech-card");

const observer = new IntersectionObserver(entries => {

    entries.forEach(entry => {

        if(entry.isIntersecting){

            entry.target.classList.add("show");

        }

    });

});

cards.forEach(card => observer.observe(card));


// Button Hover Effect

const buttons = document.querySelectorAll("button, .primary-btn, .secondary-btn");

buttons.forEach(btn=>{

    btn.addEventListener("mouseenter",()=>{

        btn.style.transform="scale(1.05)";

    });

    btn.addEventListener("mouseleave",()=>{

        btn.style.transform="scale(1)";

    });

});