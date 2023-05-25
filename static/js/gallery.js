

// Get recommendation list
const container = document.querySelector(".tm-gallery");
//const url = "서버로부터 이미지를 받아올 URL"; // 실제 URL로 대체해야 합니다.

fetch(url)
    .then((response) => response.json())
    .then((data) => {
        data.forEach((item) => {
            const link = document.createElement("a");
            link.href = "url"; // link to the content description or external link

            const figure = document.createElement("figure");
            figure.classList.add("tm-gallery-item");

            const image = document.createElement("img");
            image.classList.add("image-fluid");
            image.src = item.url;
            image.alt = item.alt;

            title = document.createElement('div');
            div.classList.add("content-title");
            div.innerHTML = item.title;

            desc = document.createElement("div");
            div.classList.add("content-description");
            div.innerHTML = item.desc;

            figure.appendChild(image);
            link.appendChild(figure);
            container.appendChild(link);
        });
    })
    .catch((error) => console.error(error));
