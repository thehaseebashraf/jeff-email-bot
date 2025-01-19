# src/response_generator.py
import os
import requests

from dotenv import load_dotenv
import os

load_dotenv() 

def generate_email_response(email_subject, email_body, similar_content):
    """
    Generate email response using OpenAI with context from similar content
    
    Args:
        email_subject: Subject of the incoming email
        email_body: Body of the incoming email
        similar_content: List of similar documents found in vector search
    
    Returns:
        Generated response text
    """
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    if not OPENAI_API_KEY:
        raise ValueError("OpenAI API key not found in environment variables")    # if not OPENAI_API_KEY:
    #     raise ValueError("OpenAI API key not found")
    
    # Format the context from similar content
    context = "\n".join([
        f"Document {i+1}:\nTitle: {doc['title']}\nContent: {doc['content']}"
        for i, doc in enumerate(similar_content)
    ])
    
    messages = [
        {
            "role": "system",
            "content": """You are the official email response agent for New City Insurance. Your role is to provide accurate, professional, and concise responses to inquiries from both customers and employees.

                            Key guidelines:
                            - Keep responses clear, direct, and under 4-5 sentences when possible
                            - Only use information provided in the context and email query
                            - Do not make assumptions or create information not present in the provided context
                            - If information is missing to address a query, clearly state what specific information is needed
                            - Use a professional but warm tone
                            - Alaways answer in bullet points
                            - Start emails with "Dear [Name]" when the sender's name is available or just use their name provided in the email
                            - Sign off with "Best regards, New City Insurance Support"

                            Response handling:
                            - For policy-specific questions: Only reference information explicitly present in the context
                            - For claim inquiries: Provide status updates or next steps based solely on provided information 
                            - For technical issues: Offer only documented solutions from the context
                            - For coverage questions: Cite only coverage details present in the support documentation

                            Important:
                            - Never speculate about policy terms, coverage, or claim outcomes
                            - Don't provide timelines or promises unless explicitly mentioned in the context
                            - Don't reference internal processes or systems unless they're in the context
                            - If you cannot answer fully with the available information, acknowledge the query and specify what additional information is needed

                            Remember: Accuracy and brevity over comprehensiveness. It's better to be clear about what you don't know than to provide uncertain information."""
        },
        {
            "role": "user",
            "content": f"""Generate an email response for the following email:
                        Subject: {email_subject}
                        Body: {email_body}
                        
                        Similar content for context:
                        {context}"""
        }
    ]
    
    try:
        response = requests.post(
            url="https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4",
                "messages": messages,
                "temperature": 0.3
            }
        )
        
        response.raise_for_status()
        response_json = response.json()
        
        if 'error' in response_json:
            raise Exception(f"OpenAI API Error: {response_json['error']}")
        
        return response_json['choices'][0]['message']['content']
    
    except requests.exceptions.RequestException as e:
        print(f"Error generating response: {str(e)}")
        raise Exception(f"API call failed: {str(e)}")