


$("#search-btn").click(async function () {
    var searchQuery = $("#search-input").val().trim();
    if (searchQuery !== "") {
        window.location.href = "/search/?q=" + encodeURIComponent(searchQuery);
        // const response = await fetch('/search/?' 
        //     + new URLSearchParams({
        //         q: searchQuery
        //     }),
        // { method: 'GET'});

        // if (!response.ok) {
        //     // something went wrong...
        // }
        // else {
        //     // redirect to search page
        //     window.location.href = "/search/?q=" + encodeURIComponent(searchQuery);
        // }
    }
});