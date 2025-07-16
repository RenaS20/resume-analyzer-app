import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file (if you're using it)
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def analyze_resume(resume_text, target_role):
    prompt = f"""
You are a hiring manager evaluating a resume for the role of {target_role}.

Evaluate the resume below and provide:
1. A score out of 5 for each of the following:
   - Action Verbs
   - Quantified Impact
   - Clarity
   - Relevance to {target_role}

2. A paragraph of constructive feedback.

3. Two improved versions of weak bullet points you find.

Resume:
\"\"\"
{resume_text}
\"\"\"
    """

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://resume-analyzer.streamlit.app",  # any name is fine
        "X-Title": "Resume Analyzer",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/mixtral-8x7b-instruct",  # free model on OpenRouter
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    
    try:
        result = response.json()
        print("✅ Response from OpenRouter:")
        print(result)

        if "choices" in result:
            return result["choices"][0]["message"]["content"]
        elif "error" in result:
            return f"❌ Error from API: {result['error'].get('message', 'Unknown error')}"
        else:
            return f"❌ Unexpected response: {result}"
    except Exception as e:
        return f"❌ Failed to parse API response: {e}"
