const hamburger = document.getElementById("nav-burger");
const themeToggler = document.getElementById("theme-toggler");
const accountMenuButton = document.getElementById("account-menu");
const accountMenu = document.getElementById("account-menu-content");
const overlay = document.getElementById("sidebar-overlay");
const hamburgerMenu = document.getElementById("hamburger-menu");
const closeBurger = document.getElementById("close-burger");

hamburger.addEventListener("click", () => {
    overlay.classList.remove("hidden");
    hamburgerMenu.classList.add("active");
});

accountMenuButton.addEventListener("click", () => {
    accountMenu.classList.toggle("hidden");
});

overlay.addEventListener("click", () => {
    hamburgerMenu.classList.remove("active");
    overlay.classList.add("hidden");
});

closeBurger.addEventListener("click", () => {
    overlay.classList.add("hidden");
    hamburgerMenu.classList.remove("active");
})

document.addEventListener("click", (event) => {
    let target = event.target;
    if (!target.closest("#account-menu") && !target.closest("#account-menu")) {
        accountMenu.classList.add("hidden");
    }
});

document.addEventListener("click", (event) => {
    let target = event.target;
    if (!target.closest("#hamburger-menu") && !target.closest("#nav-burger")) {
        overlay.classList.add("hidden");
        hamburgerMenu.classList.remove("active");
    }
});