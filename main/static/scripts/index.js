const input = document.getElementById("resumeInput");
const label = document.getElementById("fileLabel");

input.addEventListener("change", () => {
  if (input.files.length > 0) {
    label.textContent = input.files[0].name;
  } else {
    label.textContent = "Select Resume (PDF/DOCX)";
  }
});
