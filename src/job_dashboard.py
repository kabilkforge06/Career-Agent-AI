from ai_modules.llm_helper import query_llm
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_llm_query(prompt: str) -> str:
    return query_llm(prompt)

def generate_agentic_roadmap(goal: str, companies: str = "") -> str:
    if not goal.strip():
        raise ValueError("Career goal cannot be empty")

    goal = goal.lower().strip()
    companies = companies.lower().strip()

    prompt = f"""
You are a career advisor helping a student plan for their future.

Career Goal: {goal}
Preferred Companies or Industries: {companies if companies else "Any"}

Please provide in simple bullet points:
- 5 essential skills
- 2-3 recommended certifications
- 3 mock interview questions
- 2 interview success tips

Format your answer neatly.
"""
    try:
        response = cached_llm_query(prompt)
        return response
    except Exception as e:
        return f"⚠️ Error generating roadmap: {str(e)}"
