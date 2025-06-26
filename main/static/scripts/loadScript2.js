const steps = [
  { id: "step2", delay: 5000, progress: 50 },
  { id: "step3", delay: 5000, progress: 100 },
];

const progressBar = document.getElementById("progressBar");

let enhancementReady = fetch("/enhancer").then((res) => res.json());

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
      enhancementReady.then(() => {
        window.location.href = "/enhanced"; // Change this if needed
      }); // Change this if needed
    }, 1000);
  });
