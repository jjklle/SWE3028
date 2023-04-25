// 로그인 버튼 클릭 시 모달 팝업 열기
const loginBtn = document.getElementById("login-btn");
const loginModal = document.getElementById("login-modal");
const closeBtn = document.getElementsByClassName("close")[0];
const registerBtn = document.getElementById("register-btn");
const registerModal = document.getElementById("register-modal");

loginBtn.onclick = function () {
    loginModal.style.display = "block";
};

registerBtn.onclick = function () {
    loginModal.style.display = "block";
};


closeBtn.onclick = function () {
    if (loginModal !== null){
        loginModal.style.display = "none";    
    }
    else if (registerModal !== null) {    
        registerModal.style.display = "none";
    }
};

// 모달 외부 클릭 시 모달 닫기
window.onclick = function (event) {
    if (event.target == loginModal) {
        loginModal.style.display = "none";
    }
};


// login/register 다르게 구현해야함.

// login
// Crypto API를 이용한 암호화 함수
function encryptData(data, key) {
  const enc = new TextEncoder();
  const encodedData = enc.encode(data);
  return crypto.subtle.encrypt({name: 'AES-GCM', iv: new Uint8Array(12)}, key, encodedData);
}

// 폼 제출 시에 실행될 함수
async function onSubmit(event) {
  event.preventDefault();

  // ID와 PW를 가져와서 암호화
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;
  const key = await crypto.subtle.generateKey({name: 'AES-GCM', length: 256}, true, ['encrypt']);
  const encryptedUsername = await encryptData(username, key);
  const encryptedPassword = await encryptData(password, key);

  // 암호화된 데이터를 서버로 전송
  const formData = new FormData();
  formData.append('username', new Blob([encryptedUsername], {type: 'application/octet-stream'}));
  formData.append('password', new Blob([encryptedPassword], {type: 'application/octet-stream'}));
  const response = await fetch('/login', {method: 'POST', body: formData});

  // 서버로부터 응답 받음
  const data = await response.json();
  console.log(data);
}

// 폼 제출 이벤트 핸들러 등록
document.getElementById('submit').addEventListener('submit', onSubmit);
