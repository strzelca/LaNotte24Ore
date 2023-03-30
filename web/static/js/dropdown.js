// Hide dropdown on load and show when menu-button is pressed

const menuButton = document.getElementById("menu-button");
const dropdown = document.getElementById("header-dropdown");

menuButton.addEventListener("click", function () {
    if (dropdown.classList.contains("hidden")) {
        dropdown.classList.remove("hidden");
        dropdown.classList.add("absolute");
    } else {
        dropdown.classList.remove("absolute");
        dropdown.classList.add("hidden");
    }
});
