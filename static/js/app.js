document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("study-form");
  if (!form) return;

  const questionInput = document.getElementById("question");
  const submitButton = document.getElementById("submit-button");
  const modeTitle = document.getElementById("mode-title");
  const modeDescription = document.getElementById("mode-description");
  const modeLabel = document.getElementById("mode-label");
  const inputLabel = document.getElementById("input-label");
  const formHint = document.getElementById("form-hint");
  const quizOptions = document.getElementById("quiz-options");
  const numQuestions = document.getElementById("num-questions");
  const modeButtons = document.querySelectorAll(".mode-btn");

  const modes = {
    ask: {
      action: "/ask", label: "ASK", title: "Ask a question",
      description: "Ask something about the study material you provided.",
      inputLabel: "Your question",
      placeholder: "e.g. Explain the main concept in simple terms...",
      button: "Ask Question",
      hint: "Answers are generated from your study material."
    },
    summarize: {
      action: "/summarize", label: "SUMMARIZE", title: "Summarize a topic",
      description: "Enter a topic and generate a concise study summary.",
      inputLabel: "Topic",
      placeholder: "e.g. Photosynthesis, networking, machine learning...",
      button: "Generate Summary",
      hint: "The summary is based on your study material."
    },
    quiz: {
      action: "/quiz", label: "QUIZ", title: "Generate a quiz",
      description: "Choose a topic and the number of questions to practice.",
      inputLabel: "Quiz topic",
      placeholder: "e.g. Generate a quiz about TCP/IP...",
      button: "Generate Quiz",
      hint: "Choose the number of questions below."
    },
    flashcards: {
      action: "/flashcards", label: "FLASHCARDS", title: "Create flashcards",
      description: "Turn a topic into quick revision flashcards.",
      inputLabel: "Flashcard topic",
      placeholder: "e.g. Create flashcards about operating systems...",
      button: "Generate Flashcards",
      hint: "Flashcards are generated from your study material."
    }
  };

  function setMode(mode) {
    const config = modes[mode];
    if (!config) return;

    form.action = config.action;
    modeLabel.textContent = config.label;
    modeTitle.textContent = config.title;
    modeDescription.textContent = config.description;
    inputLabel.textContent = config.inputLabel;
    questionInput.placeholder = config.placeholder;
    submitButton.textContent = config.button;
    formHint.textContent = config.hint;

    const isQuiz = mode === "quiz";
    quizOptions.hidden = !isQuiz;
    numQuestions.disabled = !isQuiz;
  }

  modeButtons.forEach(button => {
    button.addEventListener("click", () => {
      modeButtons.forEach(btn => btn.classList.remove("active"));
      button.classList.add("active");
      setMode(button.dataset.mode);
    });
  });

  form.addEventListener("submit", (event) => {
    const activeButton = document.querySelector(".mode-btn.active");
    if (!activeButton) return;

    if (activeButton.dataset.mode === "quiz") {
      const count = Number(numQuestions.value);
      if (!Number.isInteger(count) || count < 1 || count > 20) {
        event.preventDefault();
        alert("Please choose between 1 and 20 questions.");
      }
    }
  });

  setMode("ask");
});
