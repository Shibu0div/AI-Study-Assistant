import boto3 
from config import AWS_REGION, KNOWLEDGE_BASE_ID

kb_client = boto3.client(
    "bedrock-agent-runtime",
    region_name = AWS_REGION
)

def retrieve_context(question,number_of_results=3):
    response = kb_client.retrieve(
        knowledgeBaseId = KNOWLEDGE_BASE_ID, 
        retrievalConfiguration = {
            "managedSearchConfiguration": {
                "numberOfResults": number_of_results
            }
        }, 
        retrievalQuery={
            "text": question
        }
    )
    results = response.get("retrievalResults",[])
    contexts = []

    for result in results:
        text = result.get("content",{}).get("text","")

        if text:
            contexts.append(text)
    return contexts