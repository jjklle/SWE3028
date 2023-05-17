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
    if (loginModal !== null){
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


// login/register 다르게 구현해야함.

// login
// Crypto API를 이용한 암호화 함수
/*
function encryptData(data, key) {
  const enc = new TextEncoder();
  const encodedData = enc.encode(data);
  return crypto.subtle.encrypt({name: 'AES-GCM', iv: new Uint8Array(12)}, key, encodedData);
}
*/
// 폼 제출 시에 실행될 함수 
async function loginSubmit(event) {
  event.preventDefault();
  
  // ID와 PW를 가져와서 암호화
  const username = document.getElementById('login-username').value;
  const password = document.getElementById('login-password').value;
  //const key = await crypto.subtle.generateKey({name: 'AES-GCM', length: 256}, true, ['encrypt']);
  //const encryptedUsername = await encryptData(username, key);
  //const encryptedPassword = await encryptData(password, key);
  // 암호화된 데이터를 서버로 전송
  const formData = new FormData();

  formData.append('username',username)
  formData.append('password',password)
  //formData.append('username', new Blob([encryptedUsername], {type: 'application/octet-stream'}));
  //formData.append('password', new Blob([encryptedPassword], {type: 'application/octet-stream'}));
  //비밀번호 암호화는 백앤드쪽에서 하겠습니다.

  const response = await fetch('/login', {method: 'POST', body: formData});
  
  // 서버로부터 응답 받음
  if(!response.ok){
    alert('Login failed. Please try again.')
    throw new Error('Login failed. Please try again.');
  }
  else {
    const data = await response.json();
    alert('Login successful! Token: ' + data.token);
    loginModal.style.display = "none"; // 로그인 성공하면 로그인 모달 닫히게
    return data
  }
}

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


    const response = await fetch('/register', {method: 'POST', body: formData});
    
    // 서버로부터 응답 받음 결과에 따라 메세지 출력
    if(!response.ok){
        alert("username already exists")
        throw new Error('username already exists');
    }
    else {
        const data = await response.json();
        alert(data.message);
        registerModal.style.display = "none"; //등록 성공하면 모달 닫히게
        // open preference page
        return data
    }
  }
// 폼 제출 이벤트 핸들러 등록
//document.getElementById('submit').addEventListener('submit', onSubmit);

document.querySelector('#login-form').addEventListener('submit', loginSubmit);
document.querySelector('#register-form').addEventListener('submit', registerSubmit);
//submit eventhandler는 form에만 붙일수 있음



