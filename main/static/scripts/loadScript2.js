const steps = [
  { id: "step2", delay: 5000, progress: 50 },
  { id: "step3", delay: 5000, progress: 100 },
];

const progressBar = document.getElementById("progressBar");

steps
  .reduce((prev, step) => {
    return prev.then(() => {
      return new Promise((resolve) => {
        setTimeout(() => {
          const el = document.getElementById(step.id);
          el.classList.add("active");
          progressBar.style.width = `${step.progress}%`;
          resolve();
        }, step.delay);
      });
    });
  }, Promise.resolve())
  .then(() => {
    setTimeout(() => {
      window.location.href = "result.html"; // Change this if needed
    }, 1000);
  });
