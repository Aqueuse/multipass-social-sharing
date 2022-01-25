function showHidePassword() {
  var password_area = document.getElementById("passwordAreaId");
  if (password_area.type === "password") {
    password_area.type = "text";
  } else {
    password_area.type = "password";
  }
}