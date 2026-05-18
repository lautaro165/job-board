import requests
import json
from django.conf import settings

class Agent:
    def __init__(self):
        self.url = getattr(settings, "OLLAMA_API_URL", "http://localhost:11434/api/generate")
        self.model = getattr(settings, "OLLAMA_MODEL_NAME", "llama3:8b-instruct-q4_K_M")
        
    def analyze_resume_compatibility(self, resume_content, job_post_info):
        system_prompt = """
            You are a Senior Technical Recruiter. Analyze the compatibility between
            the provided Resume and the Job Description. 
            Return ONLY a JSON object with these keys: 
            'match_percentage' (0-100), 'matching_skills' (list), 
            'missing_skills' (list), and 'summary' (brief explanation).
        """
        
        user_prompt = f"Resume Content: {resume_content}\n\nJob Description: {job_post_info}"
        
        data = {
            "model": self.model,
            "prompt": f"{system_prompt}\n\n{user_prompt}",
            "format": "json",
            "stream": False,
            "options": {
                "temperature": 0.0
            }
        }
        
        try:
            response = requests.post(self.url, json=data)
            response.raise_for_status()
            result = response.json().get("response", "{}")
            return json.loads(result)
        except (requests.RequestException, json.JSONDecodeError) as e:
            return {"error":"AI service error.", "details": str(e)}