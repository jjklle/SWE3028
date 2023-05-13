// 데이터 요청
// fetch("/api/users")
//     .then((response) => response.json())
//     .then((data) => {
//         console.log(data);
//         // 데이터 처리
//     })
//     .catch((error) => console.error(error));
changeByJS()

function changeByJS(position, img) {
    let x = document.getElementsByClassName("content-title")[0];
    x.innerText="Javascript"; 
    x.style.color="red";
}