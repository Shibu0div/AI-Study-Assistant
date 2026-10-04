document.addEventListener("DOMContentLoaded", () => {
  const workspace = document.querySelector(".flashcard-workspace");
  if (!workspace) return;

  const cards = JSON.parse(workspace.dataset.cards);
  const card = document.getElementById("flashcard");
  const front = document.getElementById("flashcard-front");
  const back = document.getElementById("flashcard-back");
  const count = document.getElementById("flashcard-count");
  const status = document.getElementById("card-status");
  const prev = document.getElementById("prev-card");
  const next = document.getElementById("next-card");
  const review = document.getElementById("review-card");
  const known = document.getElementById("known-card");

  let index = 0;
  let flipped = false;
  const ratings = new Array(cards.length).fill(null);

  function render() {
    const current = cards[index];
    front.textContent = current.front;
    back.textContent = current.back;
    back.hidden = !flipped;

    card.classList.toggle("flipped", flipped);
    card.querySelector(".flashcard-label").textContent =
      flipped ? "ANSWER" : "QUESTION";
    card.querySelector(".flashcard-hint").hidden = flipped;

    count.textContent = `Card ${index + 1} of ${cards.length}`;
    status.textContent = ratings[index] || "Not reviewed";

    prev.disabled = index === 0;
    next.disabled = index === cards.length - 1;
  }

  card.addEventListener("click", () => {
    flipped = !flipped;
    render();
  });

  prev.addEventListener("click", () => {
    if (index > 0) {
      index--;
      flipped = false;
      render();
    }
  });

  next.addEventListener("click", () => {
    if (index < cards.length - 1) {
      index++;
      flipped = false;
      render();
    }
  });

  review.addEventListener("click", () => {
    ratings[index] = "Needs review";
    render();
  });

  known.addEventListener("click", () => {
    ratings[index] = "✓ Known";
    render();
  });

  render();
});
