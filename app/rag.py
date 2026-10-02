from knowledge_base import retrieve_context 

from bedrock import ask_AI 

def explain_from_knowledge_base(question):
    contexts = retrieve_context(question,number_of_results=3) 
    if not contexts:
        return {
            "answer": "I don't know based on the provided study material.",
            "input_tokens": 0,
            "output_tokens": 0,
            "total_tokens": 0,
        }
    context = "\n\n---\n\n".join(contexts) 
    prompt = f'''
You are an AI study assistant.

Answer the question using ONLY the study material below.

If the answer cannot be found in the study material, say:
"I don't know based on the provided study material."

Study material:
{context}

Question:
{question}

Give a clear and concise answer.
'''
    return ask_AI(prompt,max_tokens=100)