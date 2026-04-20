const loginForm = document.querySelector(".login-form");
const signupForm = document.querySelector(".signup-form");
const loginBtn = document.querySelector(".login-btn");
const signupBtn = document.querySelector(".signup-btn");
const signupLink = document.querySelector("form .signup-link a");
const accountInformationBtn = document.getElementById("accountInformationBtn");
const accountInformationContainer = document.getElementById(
  "accountInformationContainer",
);
const workInformationContainer = document.getElementById(
  "workInformationContainer",
);
const backArrow = document.getElementById("backArrow");
signupBtn.onclick = () => {
  signupBtn.classList.add("active");
  loginBtn.classList.remove("active");
  loginForm.style.marginRight = "-120%";
};

loginBtn.onclick = () => {
  loginBtn.classList.add("active");
  signupBtn.classList.remove("active");
  loginForm.style.marginRight = "0";
};
/*
accountInformationBtn.onclick = () => {
  accountInformationContainer.classList.remove("active");
  accountInformationContainer.classList.add("prev");

  workInformationContainer.classList.remove("next");
  workInformationContainer.classList.add("active");
};

backArrow.onclick = () => {
  workInformationContainer.classList.remove("active");
  workInformationContainer.classList.add("next");

  accountInformationContainer.classList.remove("prev");
  accountInformationContainer.classList.add("active");
};

signupLink.onclick = () => {
  signupBtn.click();
  return false;
};

document
  .getElementById("registerForm")
  .addEventListener("submit", async function (e) {
    e.preventDefault(); // stop default form submission

    const formData = new FormData(this);
    const response = await fetch(this.action, {
      method: this.method,
      body: formData,
    });

    if (response.ok) {
      // ✅ success
      alert("Register success!");
      window.location.href = "/dashboard";
    } else {
      // ❌ failure
      alert("Register failed!");
    }
  });
*/
