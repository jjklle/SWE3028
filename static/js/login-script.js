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
function storeUserInfo(_token, _username, _is_login) {
    const user_info = {
        access_token: _token,
        username: _username,
        is_login: _is_login // "True" or "False"
    }
    window.localStorage.setItem('user_info',JSON.stringify(user_info));
}

// Store user information into Cookies
function storeUserInfo_cookie(_data,_username,_is_login) {
    Cookies.set('access_token',_data.token);
    Cookies.set('id',_data.id);
    Cookies.set('username',_username);
    Cookies.set('is_login',_is_login);
}

// Function to update the navigation bar after login
function updateNavbarAfterLogin(username) {
    // Remove the login button
    const loginButton = $("#login-btn");
    if (loginButton) {
        loginButton.remove();
    }

    // Remove the register button
    const registerButton = $("#register-btn");
    if (registerButton) {
        registerButton.remove();
    }

    // Create a new image element
    const userImageElement = $("<img>",{
        src: "/static/img/icons8-user-64.png",
        alt: "User Image",
        id: "user-image",
        href: "#",
        'data-toggle': "dropdown",
        class: "dropdown-toggle",
        'aria-haspopup': "true",
        'aria-expanded': "false"
    });

    const dropdownMenu = $("<div>",{
        class: "dropdown-menu dropdown-menu-right"
    }).append(
        $("<a>",{
            class: "dropdown-item",
            text: username,
            href: "mypage"
        }),
        $("<div>",{
            class: "dropdown-divider"
        }),
        $("<a>",{
            class: "dropdown-item",
            href: "#",
            id: "logout",
            text: "Logout"
        }));

    const div = $("<div>",{
        class:"dropdown"
    }).append(userImageElement,dropdownMenu);
    div.appendTo("#navbarSupportedContent ul");
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
        const data = await response.json(); // has index id and token
        alert('Login successful! Token: ' + data.token);
        loginModal.style.display = "none"; // 로그인 성공하면 로그인 모달 닫히게
        
        storeUserInfo_cookie(data,username,"True");       
      
        // remove register & login button
        // and show user information
        updateNavbarAfterLogin(username);
        
        location.reload();

        return data
    }
}

/*===Authetication===*/
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
                updateNavbarAfterLogin(user_info["username"]);
            }
        } catch (error) {
            // Failed to decode or verify the token
        }
    } else {
        // Token is not found, perform necessary actions for a non-logged-in user
    }
}


function authenticate_cookies() {
    const is_login = Cookies.get('is_login');
    if (is_login) { // if exists
        try {
            token = Cookies.get('access_token');
            // Verify and decode the JWT token
            const decodedToken = parseJwt(token);
            // Check if the token is expired
            const currentTime = Date.now() / 1000; // Convert to seconds
            if (decodedToken.exp < currentTime) {
                // Token is expired
            } else {
                // Token is valid
                updateNavbarAfterLogin(Cookies.get('username'));
            }
        } catch (error) {
            // Failed to decode or verify the token
        }
    } else {
        // Token is not found, perform necessary actions for a non-logged-in user
    }
}

/*===Logout===*/
function logout() {
    // clear localstorage and refresh
    Cookies.remove('access_token');
    Cookies.remove('id');
    Cookies.remove('username');
    Cookies.remove('is_login');
    // localStorage.removeItem('user_info');
    location.reload();
}


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
        storeUserInfo_cookie(data,username,"True");       

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


// window.addEventListener("load",() => {
//     authenticate_cookies();
//     if ($("#logout")) {
//         $("#logout").on("click",logout);
//     }
// });

// document.ready
$(function () {
    authenticate_cookies();
    if ($("#logout")) {
        $("#logout").on("click",logout);
    }
});
