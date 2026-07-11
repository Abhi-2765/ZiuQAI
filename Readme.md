backend/
│
├── app/
│   ├── main.py
│   ├── config.py
│
│   ├── api/
│   │   ├── upload.py          # upload + indexing
│   │   ├── quiz.py            # generate quiz
│   │   ├── attempt.py         # submit answers
│   │   ├── chat.py            # optional (chat with docs)
│
│   ├── services/
│   │
│   │   ├── ingestion/         # RAG ingestion pipeline
│   │   │   ├── parser.py
│   │   │   ├── chunker.py
│   │   │   ├── embedder.py
│   │   │   ├── ingest.py
│   │   │
│   │   ├── retrieval/         # context fetching
│   │   │   ├── retriever.py
│   │   │
│   │   ├── quiz/              # ⭐ CORE LOGIC
│   │   │   ├── generator.py   # generate questions
│   │   │   ├── evaluator.py   # check answers
│   │   │   ├── formatter.py   # MCQ/TF/etc
│   │   │
│   │   ├── llm/
│   │   │   ├── prompts.py     # quiz prompts
│   │   │   ├── llm_provider.py
│   │
│   │   ├── game/              # 🎮 gameplay logic
│   │   │   ├── session.py     # quiz session handling
│   │   │   ├── scoring.py
│
│   ├── graph/                 # LangGraph (QUIZ FLOW)
│   │   ├── state.py
│   │   ├── nodes/
│   │   │   ├── retrieve_context.py
│   │   │   ├── generate_questions.py
│   │   │   ├── validate_questions.py
│   │   │   ├── format_output.py
│   │   │
│   │   ├── quiz_graph.py
│
│   ├── db/
│   │   ├── postgres.py
│   │   ├── pgvector.py
│   │   ├── models/
│   │   │   ├── document.py
│   │   │   ├── chunk.py
│   │   │   ├── quiz.py
│   │   │   ├── question.py
│   │   │   ├── attempt.py
│
│   ├── schemas/
│   │   ├── upload_schema.py
│   │   ├── quiz_schema.py
│   │   ├── attempt_schema.py
│
│   ├── utils/
│   │   ├── logger.py
│   │   ├── helpers.py
│
├── uploads/
├── tests/
├── requirements.txt
├── .env