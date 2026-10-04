import boto3
from aws_backend.config import AWS_REGION, BEDROCK_MODEL_ID, MAX_OUTPUT_TOKENS 
from aws_backend.knowledge_base import retrieve_context

client = boto3.client(
    "bedrock-runtime", 
    region_name="us-east-1"
)

def ask_AI(question,max_tokens):
    response = client.converse(
        modelId = BEDROCK_MODEL_ID, 
        messages =[
            {
                "role": "user",
                "content" : [
                    {"text":question}
                ]
            }
        ],
        inferenceConfig = {
            "maxTokens" : max_tokens
        }
    )
    answer = response["output"]["message"]["content"][0]["text"]
    usage = response.get("usage",{})
    return {
        "answer" : answer, 
        "input_tokens": usage.get("inputTokens",0), 
        "output_tokens": usage.get("outputTokens",0),
        "total_tokens": usage.get("totalTokens",0),
    }
# Funtion to Explain a specific topic 
def explain_topic(topic: str):
    prompt = f'''
Explain the following topic to a student.

Topic:
{topic}

Requirements:
Use simple language.
Explain the important concepts.
Give a small example if useful.
Keep the answer concise.
'''
    return ask_AI(
        prompt,
        max_tokens=MAX_OUTPUT_TOKENS["explanation"]
    )

