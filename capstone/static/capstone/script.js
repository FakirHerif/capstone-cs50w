console.log("LOADED!")

document.addEventListener("DOMContentLoaded", function() {
const scrollTopButton = document.getElementById("scrollTopButton");

scrollTopButton.addEventListener("click", function() {
    event.preventDefault();
    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
});

const scrollBottomButton = document.getElementById("scrollBottomButton");


scrollBottomButton.addEventListener("click", () => {
    event.preventDefault();
    window.scrollTo({
    top: document.body.scrollHeight,
    behavior: "smooth"
  });
});
});