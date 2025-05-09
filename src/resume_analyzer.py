from ai_modules.llm_helper import query_llm

def analyze_resume(resume_text: str) -> str:
    prompt = f"""
You are a resume reviewer for students and fresh graduates.

Analyze the following resume:

{resume_text}

Please suggest:
- 3 strengths
- 3 weaknesses
- 2 quick improvements
- Suggest some links to online resources for each of the weaknesses and improvements.

Format the response clearly with bullet points.
"""
    try:
        response = query_llm(prompt)
        return response
    except Exception as e:
        return f"⚠️ Error analyzing resume: {str(e)}"
