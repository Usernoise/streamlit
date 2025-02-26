import os
import openai
import streamlit as st
from parse_hh import get_candidate_info, get_job_description

# Ensure the OpenAI API client is initialized properly
openai.api_key = os.getenv("OPENAI_API_KEY")

SYSTEM_PROMPT = """
Проскорь кандидата, насколько он подходит для данной вакансии.

Сначала напиши короткий анализ, который будет пояснять оценку.
Отдельно оцени качество заполнения резюме (понятно ли, с какими задачами сталкивался кандидат и каким образом их решал?). Эта оценка должна учитываться при выставлении финальной оценки - нам важно нанимать таких кандидатов, которые могут рассказать про свою работу
Потом представь результат в виде оценки от 1 до 10.
""".strip()


def request_gpt(system_prompt, user_prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Make sure the model is correct. Replace `gpt-4o` with the appropriate model.
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=1000,
        temperature=0,
    )
    return response.choices[0].message["content"]


st.title("CV Scoring App")

# Inputs for job description and CV URLs
job_description_url = st.text_area("Enter the job description URL")
cv_url = st.text_area("Enter the CV URL")

if st.button("Score CV"):
    with st.spinner("Scoring CV..."):

        # Fetch job description and CV data using the provided URLs
        job_description = get_job_description(job_description_url)
        cv = get_candidate_info(cv_url)

        # Display the job description and CV
        st.write("Job description:")
        st.write(job_description)
        st.write("CV:")
        st.write(cv)

        # Construct the prompt for GPT model
        user_prompt = f"# ВАКАНСИЯ\n{job_description}\n\n# РЕЗЮМЕ\n{cv}"

        # Get the GPT response for scoring
        response = request_gpt(SYSTEM_PROMPT, user_prompt)

        # Display the scoring result from GPT
        st.write("Evaluation result:")
        st.write(response)
