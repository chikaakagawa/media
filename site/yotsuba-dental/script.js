const hamburger = document.getElementById("hamburger");
const mainNav = document.getElementById("mainNav");

hamburger.addEventListener("click", () => {
  mainNav.classList.toggle("open");
});

mainNav.querySelectorAll("a").forEach((link) => {
  link.addEventListener("click", () => {
    mainNav.classList.remove("open");
  });
});
