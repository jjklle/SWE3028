

function make_element(item) {
    // index, category, title
    // item[0]: index
    // item[1]: category
    // item[2]: title
    path = '/static/img/image/' + item[0] + '.jpg';

    var div = $('<div>',{
        class: "gallery-item"
    }).append(
        $('<a>',{
            href: '/content/' + item[0],
            append: [
                $('<img>',{
                    src: path,
                    alt: 'Image'
                })
            ]
        }
    )).append($('<div>',{
        class: "gallery-item-title",
        text: item[2]
    }));

    return div
}

function make_content_display(content_data) {

    // remove existing elements
    $(document.documentElement).find('.gallery-item').remove();

    for (i = 0; i < content_data.length; i++) {
        cat = content_data[i][1];
        if (cat == 'm') {
            item = make_element(content_data[i]);
            item.appendTo("#movie-gallery");
        } else if (cat == 't') {
            item = make_element(content_data[i]);
            item.appendTo("#drama-gallery");
        } else if (cat == 'b') {
            item = make_element(content_data[i]);
            item.appendTo("#book-gallery");
        }
    }
};


