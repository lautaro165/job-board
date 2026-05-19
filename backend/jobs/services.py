from rest_framework.exceptions import ValidationError

from .utils.pdf_handler import extract_text_from_pdf
from .utils.info import get_job_post_info

from agent.agent_bridge import Agent


def analyze_resume_service(resume_file, job_id):
    job_post_info = get_job_post_info(job_id)
    
    if not resume_file:
        raise ValidationError("No resume file provided")

    resume_content = extract_text_from_pdf(resume_file)
    if not resume_content:
        raise ValidationError("Could not extract text from PDF")

    agent = Agent()
    analysis = agent.analyze_resume_compatibility(
        resume_content=resume_content,
        job_post_info=job_post_info
    )

    if "error" in analysis:
        raise ValidationError(analysis)
    
    return analysis

def get_jobs_by_agent_service(user_prompt):
    pass