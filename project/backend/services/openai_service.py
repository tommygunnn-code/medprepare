import os
import logging
from openai import OpenAI

def process_with_ai(content):
    """Process content using OpenAI's API to generate structured educational content."""
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    system_prompt = """You are a medical education assistant. Given some medical text content, you will:
    1. Create a concise summary
    2. Generate 5 relevant questions
    3. Provide corresponding answers to those questions
    
    Return the data in the following JSON format:
    {
        "summary": "concise summary here",
        "qa_pairs": [
            {"question": "Q1", "answer": "A1"},
            {"question": "Q2", "answer": "A2"},
            ...
        ]
    }
    """
    
    try:
        logging.info("Sending request to OpenAI with content length: %d", len(content))
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Process this medical text:\n\n{content}"}
            ],
            temperature=0.7,
            response_format={ "type": "json_object" }
        )
        
        ai_response = response.choices[0].message.content
        logging.info("Received OpenAI response: %s", ai_response)
        return ai_response
        
    except Exception as e:
        logging.error("Error in OpenAI processing: %s", str(e), exc_info=True)
        raise Exception(f"Error processing with OpenAI: {str(e)}")
