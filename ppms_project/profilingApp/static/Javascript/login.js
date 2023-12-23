function get_cred() {
    var email = document.getElementById('email').value
    var password = document.getElementById('password').value
    var user_type = document.getElementById('type').value

    for (var i = 0; i < 3; i++) {
        // check is user input matches username and password of a current index of the objPeople array
        if (user_type == 'Applicant') {
            window.location = "../Demo HTML/Applicant Perspective - Home.html"
            return
        }
        else if (user_type == 'Admission') {
            window.location = "../Demo HTML/Admission Perspective - Home.html"
            return
        }
        else if (user_type == 'Nurse') {
            window.location = "../Demo HTML/Nurse Perspective - Home.html"
            return
        }
        else if (user_type == 'Interviewer') {
            window.location = "../Demo HTML/Interviewer Perspective - Home.html"
            return
        }
    }
}