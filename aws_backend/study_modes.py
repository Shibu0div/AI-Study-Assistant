from aws_backend.knowledge_base import retrieve_context
from aws_backend.bedrock import ask_AI
import json
import re


def _parse_json_response(result):
    """Extract JSON from Nova output, including fenced JSON."""
    if isinstance(result, dict):
        text = result.get("answer", "")
    else:
        text = str(result)

    cleaned = text.strip()

    # Remove markdown code fences if the model adds them.
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned)

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # Try the first JSON object in the response.
        match = re.search(r"\{.*\}", cleaned, flags=re.DOTALL)
        if match:
            return json.loads(match.group(0))
        raise ValueError("The AI returned an invalid JSON response.")


def summarize_topic(topic):
    contexts = retrieve_context(topic, number_of_results=3)

    if not contexts:
        return {
            "answer": "I couldn't find enough information in the study material.",
            "input_tokens": 0,
            "output_tokens": 0,
            "total_tokens": 0
        }

    context = "\n\n---\n\n".join(contexts)

    prompt = f"""
You are an AI study assistant.

Create a concise study summary using ONLY the material provided below.

Study material:
{context}

Topic:
{topic}

Create:
1. A short explanation
2. The most important points
3. Important terms or concepts

Do not introduce information that is not present in the study material.
"""

    return ask_AI(prompt, max_tokens=350)


def generate_quiz(topic, num_questions=5):
    contexts = retrieve_context(topic, number_of_results=4)

    if not contexts:
        return {
            "quiz": [],
            "answer": "I couldn't find enough information in the study material.",
            "input_tokens": 0,
            "output_tokens": 0,
            "total_tokens": 0
        }

    context = "\n\n---\n\n".join(contexts)

    prompt = f"""
You are an AI study assistant.

Create exactly {num_questions} multiple-choice questions using ONLY the study
material below.

Study material:
{context}

Topic:
{topic}

Return ONLY valid JSON. Do not use Markdown code fences.

Use exactly this structure:
{{
  "questions": [
    {{
      "question": "Question text",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "correct_answer": 0,
      "explanation": "Short explanation"
    }}
  ]
}}

Rules:
- "correct_answer" is the zero-based index of the correct option.
- Exactly one option must be correct.
- Use only information supported by the study material.
- Do not repeat questions.
- Keep explanations short.
- Do not add outside information.
"""

    result = ask_AI(prompt, max_tokens=max(500, num_questions * 130))
    try:
        quiz_data = _parse_json_response(result)
    except (ValueError, json.JSONDecodeError):
        return {
            "quiz": [],
            "answer": "The quiz could not be formatted correctly. Please try again.",
            "input_tokens": result.get("input_tokens", 0) if isinstance(result, dict) else 0,
            "output_tokens": result.get("output_tokens", 0) if isinstance(result, dict) else 0,
            "total_tokens": result.get("total_tokens", 0) if isinstance(result, dict) else 0
        }

    questions = quiz_data.get("questions", [])
    if not isinstance(questions, list):
        questions = []

    # Basic validation before sending the quiz to the browser.
    valid_questions = []
    for item in questions[:num_questions]:
        if not isinstance(item, dict):
            continue

        options = item.get("options")
        correct = item.get("correct_answer")

        if (
            isinstance(item.get("question"), str)
            and isinstance(options, list)
            and len(options) == 4
            and all(isinstance(x, str) for x in options)
            and isinstance(correct, int)
            and 0 <= correct < 4
        ):
            valid_questions.append({
                "question": item["question"],
                "options": options,
                "correct_answer": correct,
                "explanation": str(item.get("explanation", ""))
            })

    result["quiz"] = valid_questions
    return result


def generate_flashcards(topic, num_cards=5):
    contexts = retrieve_context(topic, number_of_results=4)

    if not contexts:
        return {
            "cards": [],
            "answer": "I couldn't find enough information in the study material.",
            "input_tokens": 0,
            "output_tokens": 0,
            "total_tokens": 0
        }

    context = "\n\n---\n\n".join(contexts)

    prompt = f"""
You are an AI study assistant.

Create exactly {num_cards} flashcards using ONLY the study material below.

Study material:
{context}

Topic:
{topic}

Return ONLY valid JSON. Do not use Markdown code fences.

Use exactly this structure:
{{
  "cards": [
    {{
      "front": "Question or term",
      "back": "Concise answer or definition"
    }}
  ]
}}

Rules:
- Use only information supported by the study material.
- Do not repeat concepts.
- Keep answers concise.
- Do not introduce outside information.
"""

    result = ask_AI(prompt, max_tokens=max(400, num_cards * 90))
    try:
        cards_data = _parse_json_response(result)
    except (ValueError, json.JSONDecodeError):
        return {
            "cards": [],
            "answer": "The flashcards could not be formatted correctly. Please try again.",
            "input_tokens": result.get("input_tokens", 0) if isinstance(result, dict) else 0,
            "output_tokens": result.get("output_tokens", 0) if isinstance(result, dict) else 0,
            "total_tokens": result.get("total_tokens", 0) if isinstance(result, dict) else 0
        }

    cards = cards_data.get("cards", [])
    if not isinstance(cards, list):
        cards = []

    valid_cards = []
    for item in cards[:num_cards]:
        if (
            isinstance(item, dict)
            and isinstance(item.get("front"), str)
            and isinstance(item.get("back"), str)
            and item["front"].strip()
            and item["back"].strip()
        ):
            valid_cards.append({
                "front": item["front"].strip(),
                "back": item["back"].strip()
            })

    result["cards"] = valid_cards
    return result
