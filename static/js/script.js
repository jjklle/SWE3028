// 데이터 요청
// fetch("/api/users")
//     .then((response) => response.json())
//     .then((data) => {
//         console.log(data);
//         // 데이터 처리
//     })
//     .catch((error) => console.error(error));


function changeByJS(position) {
    let x = document.getElementsByClassName("content-title")[position];
    x.innerText=title; 

}