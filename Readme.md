# ZiuQAI

**ZiuQAI** is an intelligent, end-to-end platform for automatically generating, hosting, and participating in dynamic quizzes. 

## 🚀 Key Features
- **AI-Powered Generation**: Allows hosts to upload custom reference materials (PDFs, text, URLs) to serve as knowledge context for AI-driven quiz creation.
- **Dynamic Question Types**: Using an advanced orchestration pipeline, the AI intelligently formulates diverse questions (MCQs, SCQs, True/False) based on the chosen difficulty.
- **Drafts & Publishing**: Hosts have full control to preview, refine, save as drafts, and ultimately publish these quizzes for participants to take.
- **Real-Time Participation & Scoring**: Participants can register for active quizzes, submit their answers, and get scored automatically.
- **Live Leaderboards**: Track rankings and scores of participants in real-time on a live leaderboard.

## 🛠️ Tech Stack
- **Backend Tech Stack:** The backend is built with Python and **FastAPI**, providing high-performance, asynchronous REST APIs.
- **Database & Storage:** It utilizes **SQLAlchemy** ORM connected to an async **PostgreSQL** database (with `pgvector`) for robust data management.
- **AI Integration:** Integrates **LangChain** and **LangGraph** to orchestrate the complex Retrieval-Augmented Generation (RAG) and validation workflows using the **Google Gemini API**.
- **Frontend Tech Stack:** The user interface is a responsive, modern Single Page Application built using **React** and styled beautifully with **Tailwind CSS**.

## 🎯 Overall Impact
ZiuQAI eliminates the manual effort of creating assessments, seamlessly turning any learning material into an engaging, competitive quiz experience in seconds.

---

## 📂 Project Structure

### Backend Architecture Overview

```text
backend/
│
├── app/
│   ├── main.py
│   ├── config.py
│   │
│   ├── routers/             # API Endpoints
│   │   ├── auth.py          # User authentication
│   │   ├── quizes.py        # Generate and manage quizzes
│   │   ├── questions.py     # Question CRUD
│   │   ├── user_responses.py# Submit answers
│   │   ├── ingest.py        # File upload + indexing
│   │
│   ├── services/
│   │   ├── ingestion/       # RAG ingestion pipeline (parsers, chunkers, embedders)
│   │   ├── retrieval/       # Context fetching
│   │   ├── llm/             # LLM configurations & prompts
│   │   ├── core/            # Service factories & interfaces
│   │
│   ├── graph/               # LangGraph (QUIZ FLOW)
│   │   ├── state.py
│   │   ├── nodes/
│   │   │   ├── retrieve_context.py
│   │   │   ├── generate_questions.py
│   │   │   ├── validate_questions.py
│   │   │   ├── format_output.py
│   │   ├── quiz_graph.py
│   │
│   ├── db/                  # Database Connections
│   │   ├── base.py
│   │
│   ├── models/              # SQLAlchemy Models
│   │   ├── users.py
│   │   ├── quizes.py
│   │   ├── questions.py
│   │   ├── participants.py
│   │   ├── user_responses.py
│   │   ├── quiz_resource.py
│   │
│   ├── schemas/             # Pydantic validation schemas
│   ├── utils/               # Auth middleware, helpers, etc.
│
├── tests/
├── requirements.txt
├── .env
```