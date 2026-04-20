function isAtEnd(cardsContainer) {
  return (
    cardsContainer.scrollLeft + cardsContainer.clientWidth + 100 >=
    cardsContainer.scrollWidth
  );
}

function isAtStart(cardsContainer) {
  return cardsContainer.scrollLeft <= 100;
}

function leftArrowClicked(btn) {
  const cardsContainer =
    btn.parentElement.parentElement.parentElement.querySelector(
      ".cards-container-body",
    );
  const viewportWidth = window.innerWidth;
  const cardWidth = document.querySelector(".card").offsetWidth;
  const numberOfCardsShowen = parseInt(viewportWidth / cardWidth);
  const rightArrowBtn = btn.parentElement.querySelectorAll("button")[1];

  cardsContainer.scrollBy({
    left: -(cardWidth * numberOfCardsShowen + numberOfCardsShowen * 15),
    behavior: "smooth",
  });
  rightArrowBtn.disabled = false;
  btn.disabled = isAtStart(cardsContainer);
}

function rightArrowClicked(btn) {
  const cardsContainer =
    btn.parentElement.parentElement.parentElement.querySelector(
      ".cards-container-body",
    );
  const viewportWidth = window.innerWidth;
  const cardWidth = document.querySelector(".card").offsetWidth;
  const numberOfCardsShowen = parseInt(viewportWidth / cardWidth);
  const rightArrowBtn = btn.parentElement.querySelectorAll("button")[0];

  cardsContainer.scrollBy({
    left: cardWidth * numberOfCardsShowen + numberOfCardsShowen * 15,
    behavior: "smooth",
  });
  rightArrowBtn.disabled = false;
  btn.disabled = isAtEnd(cardsContainer);
}

// Footer tabs + privacy underline
function changeTab(tabId, contentId) {
  document
    .querySelectorAll(".tab-item")
    .forEach((t) => t.classList.remove("active-tab"));
  document
    .querySelectorAll(".tab-content")
    .forEach((c) => (c.style.display = "none"));
  document.getElementById(tabId).classList.add("active-tab");
  document.getElementById(contentId).style.display = "grid";
}

document.getElementById("main_page").classList.add("active");
