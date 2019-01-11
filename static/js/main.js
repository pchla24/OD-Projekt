var reglogin = document.getElementById("reglogin");
var regpassword = document.getElementById("regpassword");
var confirm_password = document.getElementById("confirm_password");
var email = document.getElementById("email");

var loginError = document.getElementById("login_error")
var emailError = document.getElementById("email_error")
var passwordError = document.getElementById("password_error")
var conPassError = document.getElementById("confirm_password_error")

var regsubmit = document.getElementById("regsubmit");


function Validate() {
  if (reglogin.value == "") {
    reglogin.style.border = "1px solid red";
    loginError.textContent = "To pole jest wymagane";
    return false;
  }

  if (email.value == "") {
    email.style.border = "1px solid red";
    emailError.textContent = "To pole jest wymagane";
    return false;
  }

  if (!email.value.includes("@")) {
    email.style.border = "1px solid red";
    emailError.textContent = "Email jest niepoprawny";
    return false;
  }

  if (regpassword.value == "") {
    regpassword.style.border = "1px solid red";
    passwordError.textContent = "To pole jest wymagane";
    return false;
  }

  if (confirm_password.value == "") {
    confirm_password.style.border = "1px solid red";
    conPassError.textContent = "To pole jest wymagane";
    return false;
  }

  if (regpassword.value != confirm_password.value) {
    confirm_password.style.border = "1px solid red";
    conPassError.textContent = "Hasła nie są identyczne"
    return false;
  }
}

function loginVerify() {
  if (reglogin.value != "") {
    reglogin.style.border = "1px solid #ccc";
    loginError.innerHTML = "";
    return true;
  }
}

function emailVerify() {
  if (email.value != "") {
    email.style.border = "1px solid #ccc";
    emailError.innerHTML = "";
    return true;
  }
}

function passwordVerify() {
  if (regpassword.value != "") {
    regpassword.style.border = "1px solid #ccc";
    passwordError.innerHTML = "";
    return true;
  }
}

function conPasswordVerify() {
  if (confirm_password.value != "") {
    confirm_password.style.border = "1px solid #ccc";
    conPassError.innerHTML = "";
    return true;
  }
}

reglogin.addEventListener("blur", loginVerify);
email.addEventListener("blur", emailVerify);
regpassword.addEventListener("blur", passwordVerify);
confirm_password.addEventListener("blur", conPasswordVerify);