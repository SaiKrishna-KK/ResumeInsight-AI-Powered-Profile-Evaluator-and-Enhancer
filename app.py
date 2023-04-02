from flask import Flask, render_template, request, jsonify
import openai
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)

# Set the API key from the environment variable
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/")
def index():
    return render_template("index.html")

def summarizer(input_text):
    try:
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
        {"role": "system", "content": "Please carefully read the following text and extract the most important and relevant information. Generate a concise and accurate summary of the content that is no longer than 1780 tokens. Make sure to maintain the original meaning and context of the text while focusing on the key points and themes."},
        {"role": "user", "content": f'Text to be summarized: {input_text}'},
    ],
        temperature=0.7,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )

        evaluation = response.choices[0].message['content']
        return evaluation

    except Exception as error:
        print(error)
        return jsonify({"error": "There was an error processing the request in summarizer."}), 500

@app.route("/api/evaluate", methods=["POST"])
def evaluate():
    job_description = request.json["jobDescription"]
    resume = request.json["resume"]
    job_sum = summarizer(job_description)
    resume_sum = summarizer(resume)
    


    prompt = """I want you to act as a Resume Evaluator and Suggester, and you are helping the user to develop a stronger profile. As you evaluate the resume, compare it to the job profile by focusing on the following categories: education, work experience, skills, achievements, and personal qualities. For each category, provide a brief assessment and a score out of 10, with 10 being a perfect match and 0 being no match at all. 

Once you've assessed each category, calculate the overall percentage score reflecting how well the candidate's resume aligns with the job profile. This score should be based on a weighted average of the individual category scores, considering their importance for the specific job.

In addition to providing scores, offer suggestions for improvement in each category, such as highlighting relevant achievements, rephrasing sections, or emphasizing certain qualifications. Your goal is to help job seekers present themselves in the best possible light by providing honest and constructive feedback.
Format of GENRERATED RESPONSE:
Strictly, provide your complete evaluation inside the JSON file and it should strictly have the following JSON format: 
{
  "education": {
    "score": [Education Score out of 10],
    "assessment": “[Brief assessment of Education]“,
    "suggestions": [
      "Suggestion 1 for education”,
      "Suggestion 2 for education“
    ]
  },
  "work_experience": {
    "score": [Work Experience Score out of 10],
    "assessment": “[Brief assessment of Work Experience]“,
    "suggestions": [
      "Suggestion 1 for Work Experience”,
      "Suggestion 2 for Work Experience“
    ]
  },
  "skills": {
   "score": [Skills Score out of 10],
    "assessment": “[Brief assessment of Skills]“,
    "suggestions": [
      "Suggestion 1 for Skills”,
      "Suggestion 2 for Skills“
    ]
  },
  "achievements": {
    "score": [Achievements Score out of 10],
    "assessment": “[Brief assessment of Achievements]“,
    "suggestions": [
      "Suggestion 1 for Achievements”,
      "Suggestion 2 for Achievements“
    ]
  },
  "personal_qualities": {
    "score": [Personal Qualities Score out of 10],
    "assessment": “[Brief assessment of Personal Qualities]“,
    "suggestions": [
      "Suggestion 1 for Personal Qualities”,
      "Suggestion 2 for Personal Qualities“
    ]
  },
  "overall_percentage_score": [Calculated weighted average out of 100],
  "extra_suggestions": “[All extra suggestions]”
}
"""

    try:
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
        {"role": "system", "content": prompt},
        {"role": "user", "content": f'Job Description: {job_sum}'},
        {"role": "system", "content": "Please provide me with your resume, so that I can give my evaluation."},
        {"role": "user", "content": f'Resume: {resume_sum}'}
    ],
        temperature=0.7,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )

        evaluation = response.choices[0].message['content']
        return jsonify({"evaluation": evaluation})

    except Exception as error:
        print(error)
        return jsonify({"error": "There was an error processing the request."}), 500


if __name__ == "__main__":
    app.run(debug=True)
