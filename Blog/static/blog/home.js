window.addEventListener("load", function() {
    
    let alertBox = document.getElementById("alertBox");
    if (alertBox) {
        setTimeout(function() {
            alertBox.style.display = "block";
        }, 1000); 

        setTimeout(function() {
            alertBox.style.display = "none";
        }, 3000); 
    } else {
        console.error("Element with id 'alertBox' not found.");
    }
});
