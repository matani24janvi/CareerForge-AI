import google.generativeai as genai
import json

def call_gemini_on(text):
    genai.configure(api_key="AIzaSyD0D27Bi1Lh5toBRJnHN4T9RUh1rn1azng")

    model = genai.GenerativeModel(model_name="models/gemini-2.5-flash")


    prompt = f"""
    You are an expert resume editor and career consultant. 
    Your task is to enhance the clarity, impact, and professionalism of a candidate’s resume.

    When provided with the full resume text, return an improved version that:

    - Preserves all original information
    - Rewrites sentences and bullet points for stronger phrasing and clarity
    - Improves action verb usage and impact wording
    - Fixes inconsistent formatting
    - Organizes sections logically (Education, Skills, Projects, etc.)
    - Keeps it concise and ATS-friendly

    Only return the enhanced resume in clean markdown-style format with proper section headers. 
    Do not include suggestions, feedback, or a summary—just return the improved resume.

    Resume:
    \"\"\"{text}\"\"\"
    """

    # 🚀 Generate enhanced resume
    response = model.generate_content(prompt)

    return response.text