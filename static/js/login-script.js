/*=== Modal functions ===*/
// 로그인 버튼 클릭 시 모달 팝업 열기
const loginBtn = document.getElementById("login-btn");
const loginModal = document.getElementById("login-modal");
const closeBtn = document.getElementsByClassName("close")[0];
const closeBtn_reg = document.getElementsByClassName("close")[1];

const registerBtn = document.getElementById("register-btn");
const registerModal = document.getElementById("register-modal");

loginBtn.onclick = function () {
    if (registerModal.style.display !== null) {
        registerModal.style.display = "none";
    }
    loginModal.style.display = "block";
};

registerBtn.onclick = function () {
    if (loginModal.style.display !== null) {
        loginModal.style.display = "none";
    }
    registerModal.style.display = "block";
};


closeBtn.onclick = function () {
    if (loginModal !== null) {
        loginModal.style.display = "none";
    }
};

closeBtn_reg.onclick = function () {
    if (registerModal !== null) {
        registerModal.style.display = "none";
    }
};

// 모달 외부 클릭 시 모달 닫기
window.onclick = function (event) {
    if (event.target == loginModal) {
        loginModal.style.display = "none";
    }
    else if (event.target == registerModal) {
        registerModal.style.display = "none";
    }
};



/*===Login===*/
// Store user information into local storage
function storeUserInfo(token, _username, _is_login) {
    const user_info = {
        access_token: token,
        username: _username,
        is_login: _is_login // "True" or "False"
    }
    window.localStorage.setItem('user_info',JSON.stringify(user_info));
}

// Function to update the navigation bar after login
function updateNavbarAfterLogin() {
    // Remove the login button
    const loginButton = document.getElementById("login-btn");
    if (loginButton) {
        loginButton.remove();
    }

    // Remove the register button
    const registerButton = document.getElementById("register-btn");
    if (registerButton) {
        registerButton.remove();
    }

    //const userInfoElement = document.createElement("div");
    //userInfoElement.textContent = `Welcome, ${username}`;
    //userInfoElement.classList.add("nav-link","tm-nav-link");
    
    // Create a new image element
    const userImageElement = document.createElement("img");
    userImageElement.src = "/static/img/icons8-user-64.png";
    userImageElement.alt = "User Image";
    userImageElement.id = 'user-image';

    // Append the image element to the navbar
    const navbar = document.getElementById("navbarSupportedContent");
    if (navbar) {
        navbar.appendChild(userImageElement);
    }
}


// login
// 폼 제출 시에 실행될 함수 
async function loginSubmit(event) {
    event.preventDefault();

    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;
    const formData = new FormData();
    formData.append('username',username)
    formData.append('password',password)

    const response = await fetch('/login',{ method: 'POST',body: formData });

    // 서버로부터 응답 받음
    if (!response.ok) {
        alert('Login failed. Please try again.')
        throw new Error('Login failed. Please try again.');
    }
    else {
        const data = await response.json();
        alert('Login successful! Token: ' + data.token);
        loginModal.style.display = "none"; // 로그인 성공하면 로그인 모달 닫히게
        
        storeUserInfo(data.token,username,"True");       
      
        // remove register & login button
        // and show user information
        updateNavbarAfterLogin();
        
        // send request to server->get recommendation lists
        const response2 = fetch('/recommend',{ method: 'POST',body: JSON.stringify(username) });
        const recommend_ls = await response2;
        console.log(recommend_ls);


        return data
    }
}

/*===Authetication===*/
// function parseJwt(token) {
//     var base64Url = token.split('.')[1];
//     var base64 = base64Url.replace(/-/g,'+').replace(/_/g,'/');
//     var jsonPayload = decodeURIComponent(window.atob(base64).split('').map(function (c) {
//         return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
//     }).join(''));

//     return JSON.parse(jsonPayload);
// }
function parseJwt(jwt) {
    var token = jwt.split(".")[1];
    return JSON.parse(atob(token));
}

//test
// const storage = localStorage.getItem('user_info');
// const user_info = JSON.parse(storage);
// const decodedToken = parseJwt(user_info["access_token"]);
// console.log(decodedToken);

function authenticate() {
    const storage = localStorage.getItem('user_info');
    const user_info = JSON.parse(storage);
    if (user_info) { // if exists
        try {
            // Verify and decode the JWT token
            const decodedToken = parseJwt(user_info["access_token"]);
            // Check if the token is expired
            const currentTime = Date.now() / 1000; // Convert to seconds
            if (decodedToken.exp < currentTime) {
                // Token is expired
            } else {
                // Token is valid
                updateNavbarAfterLogin();
            }
        } catch (error) {
            // Failed to decode or verify the token
        }
    } else {
        // Token is not found, perform necessary actions for a non-logged-in user
    }
}
window.addEventListener("load",() => {
    authenticate();
});


/*===Register===*/
async function registerSubmit(event) {
    event.preventDefault();

    // ID와 PW를 가져와서 암호화
    const username = document.getElementById('reg-username').value;
    const password = document.getElementById('reg-password').value;
    const confirm_password = document.getElementById('confirm-password').value;
    const email = document.getElementById('email').value;
    const formData = new FormData();

    formData.append('username',username)
    formData.append('password',password)
    formData.append('email',email)

    //유저가 입력 제대로 했는지 확인
    if (username.length === 0) {
        alert('아이디를 입력해주세요')
        return
    } else if (password.length === 0) {
        alert('비밀번호를 입력해주세요.')
        return
    } else if (confirm_password.length === 0) {
        alert('비밀번호를 재입력해주세요.')
        return
    } else if (email.length === 0) {
        alert('이메일을 입력해주세요.')
        return
    }

    // 비밀번호, 재입력 비밀번호 일치 확인
    if (password !== confirm_password) {
        alert('비밀번호가 일치하지 않습니다.')
        return
    }


    const response = await fetch('/register',{ method: 'POST',body: formData });

    // 서버로부터 응답 받음 결과에 따라 메세지 출력
    if (!response.ok) {
        alert("username already exists")
        throw new Error('username already exists');
    }
    else {
        const data = await response.json();
        registerModal.style.display = "none"; // 등록 성공하면 모달 닫히게
        
        // localstorage
        storeUserInfo(data.token,username,"True");       

        // open preference page
        try {
            const response = await fetch('/register/preference',{
                method: 'GET',
                credentials: 'include', // Include cookies in the request
            });

            if (response.ok) {
                // Redirect to the preference page
                window.location.href = '/register/preference';
            } else {
                window.location.href = '/error'
            }
        } catch (error) {
        }
    }
}

document.querySelector('#login-form').addEventListener('submit',loginSubmit);
document.querySelector('#register-form').addEventListener('submit',registerSubmit);




