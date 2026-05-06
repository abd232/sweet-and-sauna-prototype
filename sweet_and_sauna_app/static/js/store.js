const searchInput = document.getElementById("search");
const categoryFilter = document.getElementById("category-filter");
const sortFilter = document.getElementById("sort-filter");
const minRange = document.getElementById("min-range");
const maxRange = document.getElementById("max-range");
const productsContainer = document.getElementById("products-grid");
const productsCount = document.getElementById("products-count");
const fromVal = document.getElementById("from-val");
const toVal = document.getElementById("to-val");

const progress = document.getElementById("progress");

function updatePriceLabels() {
  fromVal.textContent = `₪${minRange.value}`;
  toVal.textContent = `₪${maxRange.value}`;
  updateProgress();
}

function updateProgress() {
  const min = parseInt(minRange.min);
  const max = parseInt(minRange.max);

  const left = ((minRange.value - min) / (max - min)) * 100;
  const right = ((maxRange.value - min) / (max - min)) * 100;

  progress.style.right = left + "%";
  progress.style.left = 100 - right + "%";
}

minRange.addEventListener("input", function () {
  if (parseInt(minRange.value) > parseInt(maxRange.value)) {
    minRange.value = maxRange.value;
  }
  updatePriceLabels();
});

maxRange.addEventListener("input", function () {
  if (parseInt(maxRange.value) < parseInt(minRange.value)) {
    maxRange.value = minRange.value;
  }
  updatePriceLabels();
});

updatePriceLabels();

function getSelectedTags() {
  const selectedTags = document.querySelectorAll(".tag-button.selected");
  return Array.from(selectedTags).map((tag) => tag.dataset.tagId);
}

function fetchFilteredProducts(page = 1) {
  const params = new URLSearchParams();

  params.append("search", searchInput.value);
  params.append("category", categoryFilter.value);
  params.append("min_price", minRange.value);
  params.append("max_price", maxRange.value);
  params.append("sort", sortFilter.value);

  const selectedTags = getSelectedTags();
  selectedTags.forEach((tagId) => {
    params.append("tags[]", tagId);
  });

  fetch(`/store/filter/?${params.toString()}&page=${page}`, {
    method: "GET",
    headers: {
      "X-Requested-With": "XMLHttpRequest",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Filter response:", data);
      productsContainer.innerHTML = data.html;
      productsCount.textContent = data.count;
      initQuantityButtons();
    })
    .catch((error) => {
      console.error("Filter error:", error);
    });
}

document.addEventListener("click", function (e) {
  const btn = e.target.closest(".ajax-page-btn");

  if (!btn) return;

  e.preventDefault();

  const page = btn.dataset.page;
  fetchFilteredProducts(page);
});

function debounce(func, delay = 400) {
  let timeout;
  return function () {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(), delay);
  };
}

const debouncedFetch = debounce(() => fetchFilteredProducts(1), 400);

searchInput.addEventListener("input", debouncedFetch);
categoryFilter.addEventListener("change", () => fetchFilteredProducts(1));
sortFilter.addEventListener("change", () => fetchFilteredProducts(1));

minRange.addEventListener("input", () => {
  if (+minRange.value > +maxRange.value) {
    minRange.value = maxRange.value;
  }
  updatePriceLabels();
  fetchFilteredProducts(1);
});

maxRange.addEventListener("input", () => {
  if (+maxRange.value < +minRange.value) {
    maxRange.value = minRange.value;
  }
  updatePriceLabels();
  fetchFilteredProducts(1);
});

function toggleTag(element) {
  element.classList.toggle("selected");
  fetchFilteredProducts(1);
}

function initQuantityButtons() {
  document.querySelectorAll(".product-card").forEach((card) => {
    const minusBtn = card.querySelector(".minus");
    const plusBtn = card.querySelector(".plus");
    const qtyInput = card.querySelector(".qty-input");

    if (minusBtn && plusBtn && qtyInput) {
      minusBtn.addEventListener("click", () => {
        let currentValue = parseInt(qtyInput.value) || 1;
        if (currentValue > 1) qtyInput.value = currentValue - 1;
      });

      plusBtn.addEventListener("click", () => {
        let currentValue = parseInt(qtyInput.value) || 1;
        qtyInput.value = currentValue + 1;
      });
    }
  });
}

updatePriceLabels();
initQuantityButtons();

document.addEventListener("click", function (e) {
  if (e.target.classList.contains("add-to-cart-btn")) {
    const card = e.target.closest(".product-card");
    const quantity = card.querySelector(".qty-input").value;
    const productId = e.target.dataset.productId;

    console.log("Add to cart:", productId, "Quantity:", quantity);

    // later:
    // fetch('/cart/add/', { method: 'POST', body: ... })
  }
});

document.querySelectorAll(".filter-header").forEach((header) => {
  header.addEventListener("click", function () {
    console.log("hello wolrd");
    const section = this.closest(".filter-section");
    const content = section.querySelector(".filter-content");
    const icon = this.querySelector("i");

    content.classList.toggle("hidden");

    if (icon) {
      icon.classList.toggle("fa-chevron-up");
      icon.classList.toggle("fa-chevron-down");
    }
  });
});

if (window.innerWidth <= 768) {
  document.querySelectorAll(".filter-section").forEach((section) => {
    const content = section.querySelector(".filter-content");
    const icon = section.querySelector(".filter-header i");

    content.classList.add("hidden");

    if (icon) {
      icon.classList.remove("fa-chevron-up");
      icon.classList.add("fa-chevron-down");
    }
  });
}

fetchFilteredProducts(1);
