const OpenAI = require('openai');
require('dotenv').config();

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

// Function to generate AI questions
async function generateAIQuestions(sector, degree) {
  const prompt = `Generate 5 interview questions for a ${degree} ${sector} interview. Please, don't include any commas in the questions, because I cannot separate the questions!`;

  try {
    const response = await openai.chat.completions.create({
      model: "gpt-3.5-turbo",
      messages: [{ role: "user", content: prompt }],
      max_tokens: 500,
    });

    // Split questions by new lines and filter out any empty strings
    const questions = response.choices[0].message.content.split('\n').filter(q => q);
    console.log(questions);

    return questions;
  } catch (error) {
    console.error("Error generating AI questions:", error);
    throw new Error('Failed to generate AI questions');
  }
}

module.exports = generateAIQuestions; // Export the function
