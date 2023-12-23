function get_cred(type) {
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;
    var user_type = type;
    var link;
    console.log(user_type);
    switch(user_type) {
        case 'Applicant': {
            link = "../Demo HTML/Applicant Perspective - Home.html";
            break;
        }
        case 'Admission': {
            link = "../Demo HTML/Admission Perspective - Home.html";
            break;
        }
        case 'Nurse': {
            link = "../Demo HTML/Nurse Perspective - Home.html";
            break;
        }
        case 'Interviewer': {
            link = "../Demo HTML/Interviewer Perspective - Home.html";
            break;
        }        
    }
    window.location.replace(link);
    return false;
}