# app.py - Streamlit app for AI Interview Coach
import os, json, re
from dotenv import load_dotenv
import streamlit as st
import openai
from prompts import SYSTEM_PROMPT_QGEN, SYSTEM_PROMPT_SIMULATOR, EVAL_PROMPT_TEMPLATE, FEW_SHOT_QA
from utils import extract_text_from_pdf, extract_text_from_docx, normalize_text, export_session_json

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    st.warning('OPENAI_API_KEY not set. Add it to .env or environment variables.')
openai.api_key = OPENAI_API_KEY

st.set_page_config(page_title='AI Interview Coach', layout='centered')
st.title('AI Interview Coach — Practice & Feedback')

st.markdown('Upload your resume (PDF/DOCX) and paste a job description. The system will generate tailored interview questions, simulate an interviewer persona, and evaluate your answers.')

col1, col2 = st.columns(2)
with col1:
    uploaded = st.file_uploader('Upload resume (pdf/docx)', type=['pdf','docx'])
with col2:
    jd = st.text_area('Paste job description (JD) here', height=200)

seniority = st.selectbox('Seniority level (affects question difficulty)', ['Entry', 'Mid', 'Senior'])

if st.button('Generate Questions'):
    if not uploaded or not jd.strip():
        st.error('Please upload a resume and paste the job description.')
    else:
        if uploaded.type == 'application/pdf':
            resume_text = extract_text_from_pdf(uploaded)
        else:
            resume_text = extract_text_from_docx(uploaded)
        resume_text = normalize_text(resume_text)
        st.subheader('Resume (preview)')
        st.write(resume_text[:1500] + ('...' if len(resume_text)>1500 else ''))

        # Build prompt for question generation
        few_shot_block = ''
        # convert few-shot examples to small block (optional)
        for ex in FEW_SHOT_QA:
            few_shot_block += f"EX_JD: {ex['jd']}\nEX_RESUME: {ex['resume']}\nEX_QUESTIONS: {ex['questions']}\n\n"

        prompt = f"{SYSTEM_PROMPT_QGEN}\n\nJob Description:\n{jd}\n\nResume:\n{resume_text}\n\nSeniority:{seniority}\n\nExamples:\n{few_shot_block}\n\nRespond in JSON."
        try:
            resp = openai.ChatCompletion.create(
                model='gpt-4o-mini',
                messages=[{'role':'system','content':SYSTEM_PROMPT_QGEN},{'role':'user','content':prompt}],
                temperature=0.2,
                max_tokens=500
            )
            content = resp['choices'][0]['message']['content']
        except Exception as e:
            st.error(f'OpenAI API error: {e}')
            st.stop()

        # try parse JSON
        try:
            qjson = json.loads(content)
            questions = qjson.get('questions', [])
        except Exception:
            # fallback: split by newlines
            questions = [line.strip('- ') for line in content.split('\n') if line.strip()][:8]

        st.success(f'Generated {len(questions)} questions')
        st.session_state['questions'] = questions
        st.session_state['resume'] = resume_text
        st.session_state['jd'] = jd
        st.session_state['session'] = {'questions': questions, 'answers': []}
        st.experimental_rerun()

if 'questions' in st.session_state:
    questions = st.session_state['questions']
    st.subheader('Interview Simulator')
    idx = st.number_input('Question #', min_value=1, max_value=len(questions), value=1)
    q = questions[idx-1]
    st.markdown(f"**Q{idx}:** {q}")
    answer = st.text_area('Type your answer here (or paste transcript)', height=200, key=f'ans_{idx}')
    if st.button('Submit Answer', key=f'submit_{idx}'):
        if not answer.strip():
            st.error('Please type an answer before submitting.')
        else:
            # Build evaluation prompt
            system = SYSTEM_PROMPT_SIMULATOR
            prompt = EVAL_PROMPT_TEMPLATE.format(system=system, jd=st.session_state['jd'], resume=st.session_state['resume'], question=q, answer=answer)
            try:
                resp = openai.ChatCompletion.create(
                    model='gpt-4o-mini',
                    messages=[{'role':'system','content':system},{'role':'user','content':prompt}],
                    temperature=0.2,
                    max_tokens=400
                )
                content = resp['choices'][0]['message']['content']
            except Exception as e:
                st.error(f'OpenAI API error during evaluation: {e}')
                st.stop()

            # parse eval JSON
            try:
                eval_json = json.loads(content)
            except Exception:
                # fallback: place entire response as detailed_feedback
                eval_json = {'score': None, 'strengths': [], 'improvements': [], 'detailed_feedback': content}

            st.write('**Evaluation**')
            st.write(eval_json)

            # save to session
            st.session_state['session']['answers'].append({'question': q, 'answer': answer, 'evaluation': eval_json})
            st.success('Saved answer & evaluation to session.')

    if st.button('Export Session (JSON)'):
        bio = export_session_json(st.session_state['session'])
        st.download_button('Download session.json', data=bio, file_name='interview_session.json', mime='application/json')
