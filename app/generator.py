# import os
# import json
# import requests
# from app.config import AWS_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

# # Claude Sonnet 3.5 via Amazon Bedrock endpoint
# BEDROCK_API_URL = f"https://bedrock-runtime.{AWS_REGION}.amazonaws.com/model/anthropic.claude-3-sonnet/invoke"

# headers = {
#     "Content-Type": "application/json",
#     "X-Amz-Target": "AmazonBedrockRuntime.InvokeModel",
#     "X-Amz-Region": AWS_REGION,
#     "X-Amz-AccessKeyId": AWS_ACCESS_KEY_ID,
#     "X-Amz-SecretAccessKey": AWS_SECRET_ACCESS_KEY
# }

# def build_prompt(query, retrieved_docs):
#     """
#     Constructs a prompt for Claude using the query and legal context.
#     """
#     context_text = "\n---\n".join(
#         [doc["metadata"]["text"] for doc in retrieved_docs if "metadata" in doc]
#     )

#     prompt = (
#         f"You are an expert legal assistant specialized in Indian traffic law.\n"
#         f"Answer clearly and cite relevant law or judgment if possible.\n\n"
#         f"Context:\n{context_text}\n\n"
#         f"User Query: {query}\n"
#         f"Answer:"
#     )
#     return prompt

# def get_claude_response(prompt):
#     """
#     Sends the prompt to Claude Sonnet 3.5 via Bedrock API and returns the answer.
#     """
#     body = {
#         "body": json.dumps({
#             "prompt": prompt,
#             "max_tokens_to_sample": 1024,
#             "temperature": 0.2,
#             "top_p": 0.9,
#             "stop_sequences": ["\n\n"],
#             "anthropic_version": "bedrock-2023-05-31"
#         })
#     }

#     url = BEDROCK_API_URL
#     response = requests.post(url, headers=headers, json=body)
#     response.raise_for_status()

#     result = response.json()
#     return result.get("completion", "[No response from Claude]")

# def generate_answer(query, retrieved_docs):
#     """
#     Combines prompt creation and LLM response to return final answer.
#     """
#     prompt = build_prompt(query, retrieved_docs)
#     return get_claude_response(prompt)



# import os
# import json
# import boto3
# from dotenv import load_dotenv

# load_dotenv()

# AWS_REGION = os.getenv("AWS_REGION")
# AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
# AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

# client = boto3.client(
#     "bedrock-runtime",
#     region_name=AWS_REGION,
#     aws_access_key_id=AWS_ACCESS_KEY_ID,
#     aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
# )

# def build_prompt(query, context_docs):
#     context_blocks = "\n\n".join(
#         f"{i+1}. {doc['metadata']['text']}" for i, doc in enumerate(context_docs)
#     )
#     return (
#         f"Human: You are an expert assistant in Indian traffic law.\n"
#         f"Here are relevant legal excerpts:\n\n{context_blocks}\n\n"
#         f"Now answer this query in clear language:\n{query}\n\nAssistant:"
#     )

# def generate_answer(query, context_docs):
#     prompt = build_prompt(query, context_docs)
#     body = json.dumps({
#         "prompt": prompt,
#         "max_tokens": 1024,
#         "temperature": 0.3,
#         "top_k": 50,
#         "top_p": 0.9,
#         "stop_sequences": ["\n\nHuman:"]
#     })

#     response = client.invoke_model(
#         modelId="anthropic.claude-3-sonnet-20240229-v1:0",
#         body=body,
#         contentType="application/json"
#     )

#     return response["body"].read().decode("utf-8")

import os
import json
import boto3
from dotenv import load_dotenv

load_dotenv()

# --- Configuration ---
AWS_REGION = os.getenv("AWS_REGION", "us-east-1") # Default to us-east-1 if missing
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

# Initialize Bedrock Client
client = boto3.client(
    "bedrock-runtime",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

def format_context(context_docs):
    """
    Formats retrieved documents into a clear string with sources.
    """
    formatted_text = ""
    for i, doc in enumerate(context_docs):
        # Handle cases where text might be in 'text' key or inside 'metadata'
        content = doc.get("metadata", {}).get("text") or doc.get("text", "")
        source = doc.get("metadata", {}).get("source", "Unknown File")
        
        formatted_text += f"[Source #{i+1}: {source}]\n{content}\n\n"
    return formatted_text

def generate_answer(query, context_docs):
    """
    Generates an answer using Claude 3 Sonnet on AWS Bedrock.
    """
    # 1. Prepare Context
    context_text = format_context(context_docs)
    
    # 2. Define System Instruction (The "Persona")
    system_prompt = (
        "You are an expert legal assistant specializing in Indian Traffic Laws (Motor Vehicles Act) "
        "and relevant court cases. \n"
        "Instructions:\n"
        "- Answer the user's question strictly based on the provided Context.\n"
        "- If the answer is found in the context, cite the Source file name (e.g., 'According to RA_2019.pdf...').\n"
        "- If the answer is not in the context, state that you do not have that information.\n"
        "- Keep the tone professional and legal."
    )

    # 3. Construct the Message Payload (Claude 3 Structure)
    # Claude 3 uses 'messages' list + 'system' parameter, not Human/Assistant strings.
    user_message = f"Context Data:\n{context_text}\n\nUser Question: {query}"

    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "temperature": 0.1, # Lower temperature for more factual answers
        "system": system_prompt,
        "messages": [
            {
                "role": "user",
                "content": user_message
            }
        ]
    })

    try:
        # 4. Invoke Model
        response = client.invoke_model(
            modelId="anthropic.claude-3-sonnet-20240229-v1:0",
            body=body,
            contentType="application/json",
            accept="application/json"
        )

        # 5. Parse Response
        # Read the byte stream -> Decode to String -> Parse JSON -> Extract Text
        response_body = json.loads(response["body"].read())
        answer = response_body["content"][0]["text"]
        
        return answer

    except Exception as e:
        print(f"Error generating answer: {e}")
        return "I encountered an error while communicating with the AI model."