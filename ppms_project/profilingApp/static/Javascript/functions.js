// show passwords on login and registration

// login password
function showPassword() {
    var x = document.getElementById("password1");
    if (x.type === "password") {
      x.type = "text";
    } else {
      x.type = "password";
    }
  }


// registration password 
function showPassword2() {
  var x = document.getElementById("password");
  if (x.type === "password") {
    x.type = "text";
  } else {
    x.type = "password";
  }
}

// registration confirm password 
function showPassword3() {
  var x = document.getElementById("cpassword");
  if (x.type === "password") {
    x.type = "text";
  } else {
    x.type = "password";
  }
}

// Reset new password 
function showPassword4() {
  var x = document.getElementById("new_password1");
  if (x.type === "password") {
    x.type = "text";
  } else {
    x.type = "password";
  }
}

// Reset confirm new password 
function showPassword5() {
  var x = document.getElementById("new_password2");
  if (x.type === "password") {
    x.type = "text";
  } else {
    x.type = "password";
  }
}

