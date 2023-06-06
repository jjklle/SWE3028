
// get contents from server

// display


$(document).ready(function () {
    
    // content clicked
    $('.content').click(function () {
        $(this).toggleClass('selected');
    });

    // submit onclick function
    $('#submit').click(function () {
        const selected = document.getElementsByClassName("selected")
        const selected_id =[]
        Array.from(selected).forEach(item => {
            selected_id.push(item.id);
            // Perform operations on each item ID here
          });
        //console.log(selected_id)
        
        fetch('/preference', {method: 'POST', headers: {'Content-Type': 'application/json' }, body: JSON.stringify(selected_id)})
        alert('회원가입이 완료되었습니다.')
        window.location.href ='/'
        // move to index page
        // send information to the server
    });
    // 다음페이지는 없어도 될 것 같습니다.
    // next button->load more contents
    // and save the information temporarily
    $('#next').click(function () {
    });
});




