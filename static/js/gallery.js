

// // Get recommendation list
// const container = document.querySelector(".tm-gallery");
// //const url = "서버로부터 이미지를 받아올 URL"; // 실제 URL로 대체해야 합니다.

// fetch(url)
//     .then((response) => response.json())
//     .then((data) => {
//         data.forEach((item) => {
//             const link = document.createElement("a");
//             link.href = "url"; // link to the content description or external link

//             const figure = document.createElement("figure");
//             figure.classList.add("tm-gallery-item");

//             const image = document.createElement("img");
//             image.classList.add("image-fluid");
//             image.src = item.url;
//             image.alt = item.alt;

//             title = document.createElement('div');
//             div.classList.add("content-title");
//             div.innerHTML = item.title;

//             desc = document.createElement("div");
//             div.classList.add("content-description");
//             div.innerHTML = item.desc;

//             figure.appendChild(image);
//             link.appendChild(figure);
//             container.appendChild(link);
//         });
//     })
//     .catch((error) => console.error(error));



/**
 *<a href="/content/{{movie[0][0]}}" class="content-link">
              <figure class=" tm-gallery-item">
                <img src="{{ url_for('static', path='img/gallery-tn-02.jpg') }}" alt="Image" class="img-fluid">
                <div class="content-title">{{movie[1][1]}}</div>
              </figure>
            </a>

    movie-gallery
 */

function make_element(item, category) {
  // item: content info in list e.g. ['3440', '알라딘']
  
  // path = '/static/img/'; //image path
  // idx = parseInt(item[0]) + 1;
  // if (category == 'm') {
  //   path = path + "movie_image/" + idx;
  // }else if (category == 't') {
  //   path = path + "tv_image/" + idx;
  // } else if (category == 'b') {
  //   path = path + "book_image/" + idx;
  // }
  path = '/static/img/image/' + item[0] + '.jpg';
  var link = $('<a>',{
    href: '/content/' + item[0],
    class: 'content-link'
  });

  var figure = $('<figure>',{
    class: 'tm-gallery-item'
  });

  var img = $('<img>',{
    src:  path,
    alt: 'Image',
    class: 'img-fluid'
  });

  var div = $('<div>',{
    class: 'content-title',
    text: item[1]
  });

  figure.append(img,div);
  link.append(figure);
  return link;
}

function make_content_display(content_data) {

  // remove existing elements
  $('#movie-gallery').find('a').remove();
  $('#drama-gallery').find('a').remove();
  $('#book-gallery').find('a').remove();

  for (i = 0; i < 8; i++) {
    item = make_element(content_data.movie[i], 'm');
    item.appendTo("#movie-gallery");

    item = make_element(content_data.drama[i], 't');
    item.appendTo("#drama-gallery");

    item = make_element(content_data.book[i], 'b');
    item.appendTo("#book-gallery");
  }
}


async function get_recommendation() {
  const response = await fetch('/recommend',{ method: 'POST' });
  if (!response.ok) {
    // something went wrong...
  }
  else {
    const json_data = await response.json();
    data = JSON.parse(json_data);
    console.log(data);

    // create DOM elements and display
    make_content_display(data);
  }
}

//document.ready
$(function () {
  get_recommendation();
})

// $(window).on("load",get_recommendation);

