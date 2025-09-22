// check value for singup/login

document.querySelector(".register-button").addEventListener("click",function (event) {
    event.preventDefault();

    // get value
    let usernameInput = document.querySelector (".username-input");
    let emailInput = document.querySelector (".email");
    let passwordInput = document.querySelector (".password-input")
    let confirmPasswordInput = document.querySelector (".password-confirm-input");
    let accontTypeInput = document.querySelector ("#EmployerRoFreelancer");
    let cityInput = document.querySelector ("#city");
    
    let username = usernameInput.value.trim();
    let email =  emailInput.value.trim();
    let password = passwordInput.value;
    let confirmPassword = confirmPasswordInput.value;
    let accontType = accontTypeInput.value;
    let city = cityInput.value;

    // check value
    if (username === "")
    {
        alert("نام کاربری الزامی است !");
        usernameInput.classList.add("error");
    }else
    {
        usernameInput.classList.remove("error");
        usernameInput.classList.add("success");
    }
    if (email === "" || !email.includes("@"))
    {
        alert("ایمیل معتبر وارد کنید !");
        emailInput.classList.add("error");
    }else
    {
        emailInput.classList.remove("error");
        emailInput.classList.add("success");
    }
    if (password === "")
    {
        alert("رمز عبور را وارد نکردید");
        passwordInput.classList.add("error");
    }
    else if (password.length < 8)
    {
        alert("رمز عبور باید حداقل 8 کاراکتر باشد!");
        passwordInput.classList.add("error");
    }
    else if (password != confirmPassword)
    {
        alert("رمز عبور و تکرار آن یکسان نیست!");
        passwordInput.classList.add("error");
        confirmPasswordInput.classList.add("error");

    }else
    {
        passwordInput.classList.remove("error");
        passwordInput.classList.add("success");
        confirmPasswordInput.classList.remove("error");
        confirmPasswordInput.classList.add("success");
    }

    if (accontType === "") {
        alert("نوع حساب را انتخاب کنید!");
        accontTypeInput.classList.add("error");
    } else {
        accontTypeInput.classList.remove("error");
        accontTypeInput.classList.add("success");
    }

    if (city === "") {
        alert("استان را انتخاب کنید!");
        cityInput.classList.add("error");
    } else {
        cityInput.classList.remove("error");
        cityInput.classList.add("success");
    }

});