// password validation in registration form and password reset form
var pass1 = document.getElementById("pass1");
var pass2 = document.getElementById("pass2");
var message = document.getElementById("msg");
var mesg = document.getElementById("messg");
var button = document.getElementById("button");


function passCheck() {
  if (pass1.value.length > 0) {
    if (
      pass1.value.length > 7 &&
      pass1.value.match(/([a-z A-Z][0-9])|([0-9][a-z A-Z]+)/)
    ) {
      pass1.style.backgroundColor = "#98FB98";
      message.innerHTML = "";
      button.disabled = true;
    } else {
      pass1.style.backgroundColor = "#FF6666";
      message.style.color = "#FF6666";
      message.innerHTML =
        "Must enter at least a 8 character alphanumeric password!";
      button.disabled = true;
      return;
    }
  } else {
    message.innerHTML = "Please enter a password";
    button.disabled = true;
    message.style.color = "#0000ff";
    pass1.style.backgroundColor = "#FFFFFF";
  }
}
function passChecker() {
  if (pass2.value.length > 0) {
    if (pass1.value == pass2.value) {
      pass2.style.backgroundColor = "#98FB98";
      mesg.style.color = "#228B22";
      mesg.innerHTML = "<b>Ok!</b>";
      button.disabled = false;
    } else {
      pass2.style.backgroundColor = "#FF6666";
      mesg.style.color = "#FF6666";
      mesg.innerHTML = "Passwords don't match";
      button.disabled = true;
    }
  } else {
    mesg.innerHTML = "Please enter password";
    button.disabled = true;
    mesg.style.color = "#0000ff";
    pass2.style.backgroundColor = "#FFFFFF";
  }
}
