import api from "../utils/api";

const cleanId = (id) => {
  const num = parseInt(id, 10);
  if (isNaN(num)) throw new Error("Invalid quiz ID");
  return num;
};

export const quizApi = {
  createQuiz: (quizData) => api.post("/quizzes/create", quizData),
  updateQuiz: (quizData) => api.put("/quizzes/update", quizData),
  deleteQuiz: (quizId) => api.delete("/quizzes/delete", { data: { quiz_id: cleanId(quizId) } }),
  getMyQuizzes: () => api.get("/quizzes/my-quizzes"),
  getMyDrafts: () => api.get("/quizzes/my-drafts"),
  getQuizDetails: (quizId) => api.get(`/quizzes/${cleanId(quizId)}`),
  publishQuiz: (quizId) => api.post(`/quizzes/${cleanId(quizId)}/publish`),
  registerForQuiz: (quizId) => api.post(`/quizzes/${cleanId(quizId)}/register`),
  getAttemptQuestions: (quizId) => api.get(`/quizzes/${cleanId(quizId)}/attempt/questions`),
  getAttemptResponses: (quizId) => api.get(`/quizzes/${cleanId(quizId)}/attempt/responses`),
  saveAttemptResponses: (quizId, responses) => api.post(`/quizzes/${cleanId(quizId)}/attempt/save`, { responses }),
  submitQuiz: (quizId, responses) => api.post(`/quizzes/${cleanId(quizId)}/attempt/submit`, { responses }),
  getLeaderboard: (quizId) => api.get(`/quizzes/${cleanId(quizId)}/leaderboard`),
  generateAIQuiz: (quizId) => api.post(`/quizzes/${cleanId(quizId)}/generate`),
};

export default quizApi;
