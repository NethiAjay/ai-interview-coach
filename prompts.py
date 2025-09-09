# prompts.py - templates for AI Interview Coach

FEW_SHOT_QA = [
    {
        "jd": "Backend Engineer: Python, REST, databases, authentication.",
        "resume": "Worked on Flask APIs, JWT auth, PostgreSQL optimizations.",
        "questions": [
            "Explain how you designed the authentication flow using JWT.",
            "How did you optimize database queries for performance?"
        ]
    },
    {
        "jd": "Data Scientist: feature engineering, model validation, Python.",
        "resume": "Built pipelines with pandas and scikit-learn; did cross-validation.",
        "questions": [
            "Describe a time when feature engineering improved model performance.",
            "How do you choose evaluation metrics for classification tasks?"
        ]
    }
]

SYSTEM_PROMPT_QGEN = """You are an experienced technical recruiter.
Given a job description and a candidate resume, generate a list of 8 interview questions
tailored to this role. Mix technical, behavioral, and system-design style questions
appropriate for the seniority implied in the JD.
Output JSON: {"questions": ["q1","q2",...]}.
"""

SYSTEM_PROMPT_SIMULATOR = """You are a professional interviewer for the role in the job description.
Ask the provided question as if in a real interview, then evaluate the candidate's answer
using these criteria: relevance, specificity, structure (STAR), impact (quantified results).
Return JSON: {"score": number (0-10), "strengths": [...], "improvements": [...], "detailed_feedback": "text"}.
"""

EVAL_PROMPT_TEMPLATE = """{system}

Job Description:\n{jd}\n\nCandidate Resume:\n{resume}\n\nQuestion:\n{question}\n\nCandidate Answer:\n{answer}\n
Please evaluate the answer and return ONLY JSON.
"""
