$(document).ready(function() {
    activeLink()
    change_label()

    const sections = document.querySelectorAll("section");
        const navLi = document.querySelectorAll(".nav-link");
        window.onscroll = () => {
        var current = "";
    
        sections.forEach((section) => {
            const sectionTop = section.offsetTop;
            if (scrollY >= sectionTop - 60) {
            current = section.getAttribute("id"); }
        });
    
        navLi.forEach((li) => {
            li.classList.remove("active");
            if (li.href.includes(current)) {
            li.classList.add('active');
            }
        });
        };
    
})

function activeLink() {
    $('.navbar-nav .nav-item a').click(function() {

        $('.nav-link').removeClass('active')
        

        $(this).closest('.nav-link').addClass('active')
    })
}

function change_label(){
    var selected = document.getElementById('type').value;

    if (String(selected) == "Admission") {
        document.getElementById('user-lbl').innerHTML = "Admission ID:";
    }
    else if (String(selected) == "Applicant") {
        document.getElementById('user-lbl').innerHTML = "Reference Number:";
    }
    else if (String(selected) == "Nurse") {
        document.getElementById('user-lbl').innerHTML = "Nurse ID:";
    }
    else if (String(selected) == "Interviewer") {
        document.getElementById('user-lbl').innerHTML = "Interviewer ID:";
    }
    console.log(selected);
}

