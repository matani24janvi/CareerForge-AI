const score = 84;
const scoreText = document.getElementById("scoreValue");
const circle = document.querySelector(".progress");
const radius = 70;
const circumference = 2 * Math.PI * radius;
const scoreCard = document.getElementById("atsBox");
const panel = document.getElementById("suggestionPanel");

circle.style.strokeDasharray = `${circumference}`;
circle.style.strokeDashoffset = `${circumference}`;

let current = 0;

const animate = setInterval(() => {
  if (current >= score) {
    clearInterval(animate);

    setTimeout(() => {
      scoreCard.classList.remove("center");
      scoreCard.classList.add("move-left");
    }, 600); // slight delay after animation
  } else {
    current++;
    scoreText.innerText = current + "%";
    const offset = circumference - (current / 100) * circumference;
    circle.style.strokeDashoffset = offset;
  }
}, 20);

function showSuggestions() {
  panel.classList.add("slide-in");
}

// ✅ Popup Logic Starts Here

// Show modal content on card click
document.getElementById("missingSkillsBtn").addEventListener("click", function () {
  showModal("<h2>Missing Skills</h2><p>These are the skills you're missing based on the job description.</p>");
});

document.getElementById("recommendedCoursesBtn").addEventListener("click", function () {
  showModal("<h2>Recommended Courses</h2><p>Here are some courses that might help you improve.</p>");
});

document.getElementById("closeModal").addEventListener("click", function () {
  document.getElementById("popupModal").style.display = "none";
});

function showModal(content) {
  document.getElementById("modalText").innerHTML = content;
  document.getElementById("popupModal").style.display = "block";
}
