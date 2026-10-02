from knowledge_base import retrieve_context 

from bedrock import ask_AI 

def summarize_topic(topic):

    contexts = retrieve_context(
        topic,
        number_of_results=3
    )

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

    contexts = retrieve_context(
        topic,
        number_of_results=4
    )

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

Create a quiz using ONLY the study material below.

Study material:
{context}

Topic:
{topic}

Create exactly {num_questions} multiple-choice questions.

For every question provide:

Question: ...
A) ...
B) ...
C) ...
D) ...
Answer: ...
Explanation: ...

Rules:
- Use only information from the study material.
- Make the questions useful for studying.
- Do not repeat questions.
- Keep explanations short.
- Do not add information that isn't supported by the study material.
"""

    return ask_AI(prompt, max_tokens=500)

def generate_flashcards(topic, num_cards=5):

    contexts = retrieve_context(
        topic,
        number_of_results=4
    )

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

Create exactly {num_cards} flashcards using ONLY the study material below.

Study material:
{context}

Topic:
{topic}

For each flashcard provide:

Front: A question or term
Back: A concise answer or definition

Rules:
- Use only information from the study material.
- Make each flashcard useful for studying.
- Do not repeat concepts.
- Keep answers concise.
- Do not introduce outside information.
"""

    return ask_AI(prompt, max_tokens=400)