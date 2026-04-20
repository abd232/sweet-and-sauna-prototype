const minInput = document.getElementById("min-range");
const maxInput = document.getElementById("max-range");
const progress = document.getElementById("progress");
const fromVal = document.getElementById("from-val");
const toVal = document.getElementById("to-val");

function updateSlider() {
  let min = parseInt(minInput.value);
  let max = parseInt(maxInput.value);

  // Prevent thumbs from crossing
  if (min > max - 50) {
    if (event?.target === minInput) {
      minInput.value = max - 50;
      min = max - 50;
    } else {
      maxInput.value = min + 50;
      max = min + 50;
    }
  }

  // Move the progress bar
  const percentLeft = (min / minInput.max) * 100;
  const percentRight = 100 - (max / maxInput.max) * 100;

  progress.style.left = percentLeft + "%";
  progress.style.right = percentRight + "%";

  // Update display text
  fromVal.innerText = "$" + min;
  toVal.innerText = "$" + max;
}
document.getElementById("store_page").classList.add("selected");

minInput.addEventListener("input", updateSlider);
maxInput.addEventListener("input", updateSlider);

// Run once on load
updateSlider();
