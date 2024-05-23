document.addEventListener("DOMContentLoaded", function() {
    // JavaScript code here
    var likes = document.getElementById("likes");
    var posts = document.getElementById("posts");

    var po = document.getElementById("po");
    var lik = document.getElementById("lik");
    var strongElements = document.querySelectorAll('strong');

    function showposts(event) {
        event.preventDefault(); // Prevent default behavior
        posts.style.display = "block";
        strongElements[0].style.color = '#008a78';
        strongElements[1].style.color = 'black';
        likes.style.display = "none";
        po.classList.add("active");
        lik.classList.remove("active");
    }

    function showlikes(event) {
        event.preventDefault(); // Prevent default behavior
        likes.style.display = "block";
        strongElements[0].style.color = 'black';
        strongElements[1].style.color = '#008a78';
        posts.style.display = "none";
        lik.classList.add("active");
        po.classList.remove("active");
    }

    po.addEventListener("click", showposts);
    lik.addEventListener("click", showlikes);

    posts.style.display = "block";
    strongElements[0].style.color = '#008a78';
    po.classList.add("active"); // Initially active
});
