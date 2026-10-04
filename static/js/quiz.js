document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("quiz-form");
  if (!form) return;

  const questions = [...document.querySelectorAll(".quiz-question")];
  const progress = document.getElementById("quiz-progress");
  const result = document.getElementById("quiz-result");
  const scoreText = document.getElementById("score-text");
  const scoreMessage = document.getElementById("score-message");
  const retry = document.getElementById("retry-quiz");

  function updateProgress() {
    const answered = questions.filter(q =>
      q.querySelector("input[type=radio]:checked")
    ).length;
    progress.textContent = `${answered} / ${questions.length} answered`;
  }

  form.addEventListener("change", updateProgress);

  form.addEventListener("submit", (event) => {
    event.preventDefault();

    let score = 0;

    questions.forEach(question => {
      const selected = question.querySelector("input[type=radio]:checked");
      const correct = Number(question.dataset.correct);
      const feedback = question.querySelector(".question-feedback");
      const heading = feedback.querySelector("strong");

      question.querySelectorAll(".quiz-option").forEach(option => {
        option.classList.remove("selected", "correct", "wrong");
        const input = option.querySelector("input");
        if (Number(input.value) === correct) {
          option.classList.add("correct");
        }
        if (selected && input === selected) {
          option.classList.add("selected");
        }
      });

      feedback.hidden = false;

      if (!selected) {
        heading.textContent = "Not answered";
      } else if (Number(selected.value) === correct) {
        score++;
        heading.textContent = "Correct";
      } else {
        heading.textContent = "Not quite";
      }

      question.querySelectorAll("input").forEach(input => {
        input.disabled = true;
      });
    });

    const percentage = Math.round((score / questions.length) * 100);
    scoreText.textContent = `${score} / ${questions.length} — ${percentage}%`;

    if (percentage === 100) {
      scoreMessage.textContent = "Excellent work. You got every question right.";
    } else if (percentage >= 70) {
      scoreMessage.textContent = "Good work. Review the questions you missed.";
    } else {
      scoreMessage.textContent = "Review the explanations and try the quiz again.";
    }

    result.hidden = false;
    result.scrollIntoView({ behavior: "smooth", block: "center" });
  });

  retry.addEventListener("click", () => {
    window.location.reload();
  });

  updateProgress();
});
