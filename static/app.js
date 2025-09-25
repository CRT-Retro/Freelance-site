// check value for singup/login


function showError(input, mesasge)
{
    input.classList.add("error");
    input.classList.remove("success");
    const errorSpan = input.nextElementSibling;
    errorSpan.innerText = mesasge;
}


function showSuccess(input)
{
    input.classList.remove("error");
    input.classList.add("success");
    const errorSpan = input.nextElementSibling;
    errorSpan.innerText = "";
}


let usernameInput = document.querySelector (".username-input");
let emailInput = document.querySelector (".email");
let passwordInput = document.querySelector (".password-input")
let confirmPasswordInput = document.querySelector (".password-confirm-input");
let accontTypeInput = document.querySelector ("#EmployerRoFreelancer");
let cityInput = document.querySelector ("#city");

let isValid = true;

usernameInput.addEventListener("input", function()
{
    if (usernameInput.value.trim() === "")
    {
        showError(usernameInput,"نام کاربری الزامی است !");
        isValid = false;
    }
    else
    {
        showSuccess(usernameInput);
    }
});

emailInput.addEventListener("input", function()
{
    if (emailInput.value.trim() === "" || !emailInput.value.trim().includes("@"))
    {
        showError(emailInput,"ایمیل معتبر وارد کنید !");
        isValid = false;
    }
    else
    {
        showSuccess(emailInput);
    }
});

passwordInput.addEventListener("input", function()
{
    if (passwordInput.value.trim() === "")
    {
        showError(passwordInput,"رمز عبور را وارد نکردید !");
        isValid = false;
    }
    else if (passwordInput.value.trim().length < 8)
    {
        showError(passwordInput,"رمز عبور باید حداقل 8 کاراکتر باشد !");
        isValid = false;

    }else
    {
        showSuccess(passwordInput);
    }
});

confirmPasswordInput.addEventListener("input", function()
{
    if (confirmPasswordInput.value.trim() != passwordInput.value.trim())
    {
        showError(confirmPasswordInput,"رمز عبور و تکرار آن یکسان نیست !");
    }
    else
    {
        showSuccess(confirmPasswordInput);
    }
});


document.querySelector(".register-button").addEventListener("click",function() 
{
    let username = usernameInput.value.trim();
    let email =  emailInput.value.trim();
    let password = passwordInput.value;
    let confirmPassword = confirmPasswordInput.value;
    let accontType = accontTypeInput.value;
    let city = cityInput.value;

    if (username === "")
    {
        showError(usernameInput,"نام کاربری الزامی است !");
        isValid = false;

    }else
    {
        showSuccess(usernameInput)
    }

    if (email === "" || !email.includes("@"))
    {
        showError(emailInput,"ایمیل معتبر وارد کنید !");
        isValid = false;
    }else
    {
        showSuccess(emailInput)
    }
    if (password === "")
    {
        showError(passwordInput,"رمز عبور را وارد نکردید !");
        isValid = false;
    }
    else if (password.length < 8)
    {
        showError(passwordInput,"رمز عبور باید حداقل 8 کاراکتر باشد !");
        isValid = false;

    }
    else if (password != confirmPassword)
    {
        showError(passwordInput,"رمز عبور و تکرار آن یکسان نیست !");
        showError(confirmPassword,"رمز عبور و تکرار آن یکسان نیست !");
        isValid = false;

    }else
    {
        showSuccess(passwordInput);
        showSuccess(confirmPasswordInput);
    }

    if (accontType === "") {
        showError(accontTypeInput,"نوع حساب را انتخاب کنید!");
    } else {
        showSuccess(accontTypeInput);
    }

    if (city === "") {
        showError(cityInput,"استان را انتخاب کنید!");
    } else {
        showSuccess(cityInput);
    }
    
});

if (isValid) {
    // send form in backend
    console.log("همه‌چی اوکیه!");
}


// document.querySelector(".register-button").addEventListener("input",function (event) {
//     event.preventDefault();

//     // get value
//     let usernameInput = document.querySelector (".username-input");
//     let emailInput = document.querySelector (".email");
//     let passwordInput = document.querySelector (".password-input")
//     let confirmPasswordInput = document.querySelector (".password-confirm-input");
//     let accontTypeInput = document.querySelector ("#EmployerRoFreelancer");
//     let cityInput = document.querySelector ("#city");
    
//     let username = usernameInput.value.trim();
//     let email =  emailInput.value.trim();
//     let password = passwordInput.value;
//     let confirmPassword = confirmPasswordInput.value;
//     let accontType = accontTypeInput.value;
//     let city = cityInput.value;

//     // check value
//     if (username === "")
//     {
//         alert("نام کاربری الزامی است !");
//         usernameInput.classList.add("error");
//     }else
//     {
//         usernameInput.classList.remove("error");
//         usernameInput.classList.add("success");
//     }
//     if (email === "" || !email.includes("@"))
//     {
//         alert("ایمیل معتبر وارد کنید !");
//         emailInput.classList.add("error");
//     }else
//     {
//         emailInput.classList.remove("error");
//         emailInput.classList.add("success");
//     }
//     if (password === "")
//     {
//         alert("رمز عبور را وارد نکردید");
//         passwordInput.classList.add("error");
//     }
//     else if (password.length < 8)
//     {
//         alert("رمز عبور باید حداقل 8 کاراکتر باشد!");
//         passwordInput.classList.add("error");
//     }
//     else if (password != confirmPassword)
//     {
//         alert("رمز عبور و تکرار آن یکسان نیست!");
//         passwordInput.classList.add("error");
//         confirmPasswordInput.classList.add("error");

//     }else
//     {
//         passwordInput.classList.remove("error");
//         passwordInput.classList.add("success");
//         confirmPasswordInput.classList.remove("error");
//         confirmPasswordInput.classList.add("success");
//     }

//     if (accontType === "") {
//         alert("نوع حساب را انتخاب کنید!");
//         accontTypeInput.classList.add("error");
//     } else {
//         accontTypeInput.classList.remove("error");
//         accontTypeInput.classList.add("success");
//     }

//     if (city === "") {
//         alert("استان را انتخاب کنید!");
//         cityInput.classList.add("error");
//     } else {
//         cityInput.classList.remove("error");
//         cityInput.classList.add("success");
//     }

// });