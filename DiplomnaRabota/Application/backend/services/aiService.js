const generateAIResponse = async (sector, answers) => {
    // Mock AI feedback based on the sector and answers
    const feedback = answers.map((answer, index) => {
        return {
            question: `Sample question ${index + 1}`,
            answer,
            feedback: `Mock AI feedback for answer: "${answer}"`
        };
    });
    return feedback;
};

module.exports = generateAIResponse;
