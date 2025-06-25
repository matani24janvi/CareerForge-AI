const score = Math.max(...recommendationsData.map((r) => r.fit));

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
    }, 600);
  } else {
    current++;
    scoreText.innerText = current + "%";
    const offset = circumference - (current / 100) * circumference;
    circle.style.strokeDashoffset = offset;
  }
}, 20);

// Show Suggestions Panel
function showSuggestions() {
  panel.classList.add("slide-in");
}

// Show Modal
function showModal(content) {
  document.getElementById("modalText").innerHTML = content;
  document.getElementById("popupModal").style.display = "block";
}

// Close Modal
document.getElementById("closeModal").addEventListener("click", function () {
  document.getElementById("popupModal").style.display = "none";
});

// Show Missing Skills for All Roles
document
  .getElementById("missingSkillsBtn")
  .addEventListener("click", function () {
    const content = `
    <h2>Missing Skills Overview</h2>
    ${recommendationsData
      .map(
        (role) => `
      <div class="role-card">
        <h3>${role.role} — ${role.fit}% Fit</h3>
        <ul>
          ${role.missing_skills.map((skill) => `<li>${skill}</li>`).join("")}
        </ul>
      </div>
    `
      )
      .join("")}
  `;
    showModal(content);
  });

// Show Recommended Courses for All Roles
document
  .getElementById("recommendedCoursesBtn")
  .addEventListener("click", function () {
    const content = `
    <h2>Recommended Courses</h2>
    ${recommendationsData
      .map(
        (role) => `
      <div class="role-card">
        <h3>${role.role} — ${role.fit}% Fit</h3>
        <ul>
          ${role.courses
            .map(
              (course) =>
                `<li><a href="${course.url}" target="_blank">${course.title}</a></li>`
            )
            .join("")}
        </ul>
      </div>
    `
      )
      .join("")}
  `;
    showModal(content);
  });
