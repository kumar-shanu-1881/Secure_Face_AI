// simple face compare frontend
// talks to detect.py running on localhost:5000


let img1File = null;
let img2File = null;

const img1Input = document.getElementById("img1Input");
const img2Input = document.getElementById("img2Input");
const preview1 = document.getElementById("preview1");
const preview2 = document.getElementById("preview2");
const compareBtn = document.getElementById("compareBtn");
const loadingDiv = document.getElementById("loading");
const resultBox = document.getElementById("resultBox");
const errorBox = document.getElementById("errorBox");

img1Input.addEventListener("change", function () {
  const file = img1Input.files[0];
  if (!file) return;
  img1File = file;
  showPreview(file, preview1);
  checkReady();
});

img2Input.addEventListener("change", function () {
  const file = img2Input.files[0];
  if (!file) return;
  img2File = file;
  showPreview(file, preview2);
  checkReady();
});

function showPreview(file, container) {
  const reader = new FileReader();
  reader.onload = function (e) {
    container.innerHTML = "<img src='" + e.target.result + "'>";
  };
  reader.readAsDataURL(file);
}

function checkReady() {
  if (img1File && img2File) {
    compareBtn.disabled = false;
  } else {
    compareBtn.disabled = true;
  }
}

compareBtn.addEventListener("click", function () {
  errorBox.style.display = "none";
  resultBox.style.display = "none";
  loadingDiv.style.display = "block";
  compareBtn.disabled = true;

  const formData = new FormData();
  formData.append("imageA", img1File);
  formData.append("imageB", img2File);

  fetch("/api/checksimilarity", {
    method: "POST",
    body: formData
  })
    .then(function (res) {
      if (!res.ok) {
        throw new Error("Server error: " + res.status);
      }
      return res.json();
    })
    .then(function (data) {
      loadingDiv.style.display = "none";
      compareBtn.disabled = false;

      document.getElementById("distanceVal").textContent = data.distance;
      document.getElementById("thresholdVal").textContent = data.threshold;

      const matchSpan = document.getElementById("matchVal");
      if (data.match) {
        matchSpan.textContent = "YES";
        matchSpan.className = "match";
      } else {
        matchSpan.textContent = "NO";
        matchSpan.className = "no-match";
      }

      resultBox.style.display = "block";
    })
    .catch(function (err) {
      loadingDiv.style.display = "none";
      compareBtn.disabled = false;
      errorBox.textContent = "Something went wrong: " + err.message + " (is detect.py running?)";
      errorBox.style.display = "block";
    });
});