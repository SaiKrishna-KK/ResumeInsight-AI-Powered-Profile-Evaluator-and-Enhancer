const express = require('express');
const axios = require('axios');
const cors = require('cors');

const app = express();
const port = 3001;

app.use(express.json());
app.use(cors());

const openaiApiKey = 'open-ai-api-key-here';

app.post('/api/evaluate', async (req, res) => {
  const { jobDescription, resume } = req.body;
  const prompt = `I want you to act as a Resume Evaluator and Suggester
As a Resume Evaluator and Suggester, your task is to assess the suitability of a candidate for a job profile and provide suggestions for improvement. For this particular task, you have been provided with a resume and a job profile. Your primary responsibility is to evaluate the candidate's resume and determine how well it aligns with the job profile.

The resume you have been provided with is a document that summarizes the candidate's education, work experience, and skills. It is an essential tool that job seekers use to showcase their qualifications to potential employers. The job profile, on the other hand, is a description of the job requirements and responsibilities. It outlines the skills, experience, and qualifications that a candidate must possess to be considered for the role.

To evaluate the candidate's resume, you should carefully compare it to the job profile and assess how closely it matches the requirements. This assessment should consider the candidate's education, work experience, and skills. You should also look for any relevant achievements or accomplishments that may demonstrate the candidate's ability to excel in the role.

After evaluating the candidate's resume, you should provide a percentage score that reflects how well it aligns with the job profile. This score should be based on a careful analysis of the candidate's qualifications and how they relate to the job requirements.

In addition to providing a score, you should also offer suggestions to the candidate on areas where they could improve their resume to better align with the job profile. These suggestions may include highlighting relevant achievements or skills, rephrasing certain sections of the resume, or emphasizing certain qualifications.

Overall, your task as a Resume Evaluator and Suggester is to help job seekers present themselves in the best possible light to potential employers by providing honest and constructive feedback on their resumes.

Job Description:
${jobDescription}

Resume:
${resume}

Evaluation and suggestions:`;
  try {
    const response = await axios.post('https://api.openai.com/v1/engines/gpt-3.5-turbo/completions', {
      prompt,
      max_tokens: 150,
      n: 1,
      stop: null,
      temperature: 0.5,
    }, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${openaiApiKey}`,
      },
    });

    res.send({ evaluation: response.data.choices[0].text.trim() });
  } catch (error) {
    console.error(error);
    res.status(500).send({ error: 'There was an error processing the request.' });
  }
});

app.listen(port, () => {
  console.log(`Server listening at http://localhost:${port}`);
});
