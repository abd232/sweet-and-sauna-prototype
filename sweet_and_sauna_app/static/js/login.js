const loginForm = document.querySelector(".login-form");
const signupForm = document.querySelector(".signup-form");
const loginBtn = document.querySelector(".login-btn");
const signupBtn = document.querySelector(".signup-btn");
const formsContainer = document.querySelector(".forms-container");

signupBtn.addEventListener("click", () => {
  signupBtn.classList.add("active");
  loginBtn.classList.remove("active");
  formsContainer.classList.add("show-signup");
});

loginBtn.addEventListener("click", () => {
  loginBtn.classList.add("active");
  signupBtn.classList.remove("active");
  formsContainer.classList.remove("show-signup");
});
