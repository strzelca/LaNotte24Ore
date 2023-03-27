// Hide dropdown on load and show when menu-button is pressed

const imageButton = document.getElementById("image");
const closeUpload = document.getElementById("close-upload");
const imageUpload = document.getElementById("file-upload");

imageButton.addEventListener("click", function () {
    if (imageUpload.classList.contains("hidden")) {
        imageUpload.classList.remove("hidden");
        imageUpload.classList.add("absolute");
    }
});

closeUpload.addEventListener("click", function () {
    if (imageUpload.classList.contains("absolute")) {
        imageUpload.classList.remove("absolute");
        imageUpload.classList.add("hidden");
    }
});
