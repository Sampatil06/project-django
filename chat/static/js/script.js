function toggleMenu() {
  const menu = document.getElementById("left-menu");
  menu.classList.toggle("collapsed");
}

function showLogin() {
  alert("Login Button Clicked!");
}

function showRegister() {
  alert("Register Button Clicked!");
}

function adjustPageScale() {
  const contentWrapper = document.querySelector(".main-content");
  const screenWidth = window.innerWidth;

  let scaleValue = 1;

  if (screenWidth >= 992 && screenWidth <= 1600) {
    scaleValue = 0.9; // Shrink by 90%
  } else if (screenWidth >= 700 && screenWidth <= 767) {
    scaleValue = 0.8; // Shrink by 80%
  } else if (screenWidth >= 600 && screenWidth < 700) {
    scaleValue = 0.75; // Shrink by 75%
  } else if (screenWidth <= 600) {
    scaleValue = 0.5; // Shrink by 50%
  }

  contentWrapper.style.transform = `scale(${scaleValue})`;
  contentWrapper.style.transformOrigin = "top";
  contentWrapper.style.overflow = "auto";
}

window.addEventListener("load", adjustPageScale);

window.addEventListener("resize", adjustPageScale);
