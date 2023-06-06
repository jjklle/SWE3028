
// function make_element(item,category) {
//   // item: content info in list e.g. ['3440', '알라딘']
  
//   path = '/static/img/image/' + item[0] + '.jpg';
//   var link = $('<a>',{
//     href: '/content/' + item[0],
//     class: "content-link"
//   });

//   var figure = $('<figure>',{
//     class: 'tm-gallery-item',
//     style: "width:170px"
//   });

//   var img = $('<img>',{
//     src:  path,
//     alt: 'Image',
//     class: 'img-fluid'
//   });

//   var div = $('<div>',{
//     class: 'content-title',
//     text: item[1]
//   });
 
//   figure.append(img,div);
//   link.append(figure);
//   return link;
// }

// function make_content_display(content_data) {

//   // remove existing elements
//   $('#movie-gallery').find('a').remove();
//   $('#drama-gallery').find('a').remove();
//   $('#book-gallery').find('a').remove();

//   for (i = 0; i < 8; i++) {
//     item = make_element(content_data.movie[i], 'm');
//     item.appendTo("#movie-gallery");

//     item = make_element(content_data.drama[i], 't');
//     item.appendTo("#drama-gallery");

//     item = make_element(content_data.book[i], 'b');
//     item.appendTo("#book-gallery");
//   }
// }


// async function get_recommendation() {
//   const response = await fetch('/recommend',{ method: 'POST' });
//   if (!response.ok) {
//     // something went wrong...
//   }
//   else {
//     const json_data = await response.json();
//     data = JSON.parse(json_data);
//     console.log(data);

//     // create DOM elements and display
//     make_content_display(data);
//   }
// }

// function add_slick() {
//   // add slick slider on window load
//   $('.tm-gallery').slick({
//     dots: true,
//     infinite: false,
//     slidesToShow: 5,
//     slidesToScroll: 2,
//     responsive: [
//       {
//         breakpoint: 1199,
//         settings: {
//           slidesToShow: 4,
//           slidesToScroll: 2
//         }
//       },
//       {
//         breakpoint: 991,
//         settings: {
//           slidesToShow: 3,
//           slidesToScroll: 2
//         }
//       },
//       {
//         breakpoint: 767,
//         settings: {
//           slidesToShow: 2,
//           slidesToScroll: 1
//         }
//       },
//       {
//         breakpoint: 480,
//         settings: {
//           slidesToShow: 1,
//           slidesToScroll: 1
//         }
//       }
//     ]
//   });
// }

// //document.ready
// $(function () {
//   get_recommendation();

// })

// $(window).on("load",() => {
//   add_slick();
//   // 슬라이더 업데이트
//   $('.tm-gallery').slick('refresh');
// });



function make_element(item,category) {
  // item: content info in list e.g. ['3440', '알라딘']

  var path = '/static/img/image/' + item[0] + '.jpg';
  var link = $('<a>',{
    href: '/content/' + item[0],
    class: "content-link"
  });

  var figure = $('<figure>',{
    class: 'tm-gallery-item',
    style: "width:170px"
  });

  var img = $('<img>',{
    src: path,
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
    var item = make_element(content_data.movie[i],'m');
    item.appendTo("#movie-gallery");

    item = make_element(content_data.drama[i],'t');
    item.appendTo("#drama-gallery");

    item = make_element(content_data.book[i],'b');
    item.appendTo("#book-gallery");
  }
}

function add_slick() {
  // add slick slider
  $('.tm-gallery').slick({
    dots: true,
    infinite: false,
    slidesToShow: 5,
    slidesToScroll: 2,
    responsive: [
      {
        breakpoint: 1199,
        settings: {
          slidesToShow: 4,
          slidesToScroll: 2
        }
      },
      {
        breakpoint: 991,
        settings: {
          slidesToShow: 3,
          slidesToScroll: 2
        }
      },
      {
        breakpoint: 767,
        settings: {
          slidesToShow: 2,
          slidesToScroll: 1
        }
      },
      {
        breakpoint: 480,
        settings: {
          slidesToShow: 1,
          slidesToScroll: 1
        }
      }
    ]
  });
}

async function get_recommendation() {
  const response = await fetch('/recommend',{ method: 'POST' });
  if (!response.ok) {
    // something went wrong...
  } else {
    const json_data = await response.json();
    var data = JSON.parse(json_data);
    console.log(data);

    // create DOM elements and display
    make_content_display(data);

    // 슬라이더 초기화
    add_slick();
  }
}

$(function () {
  get_recommendation();
});
