🧠 Semantic Question Answering System (RAG-based)

A lightweight Retrieval-Augmented Generation (RAG) system built with Django and PostgreSQL.

This project demonstrates how to design a scalable backend architecture for semantic document retrieval and answer generation without relying on external LLM APIs during development.

🚀 Overview

The system follows a simplified RAG pipeline:

User submits a question

Relevant documents are retrieved using PostgreSQL Full-Text Search

Top-ranked documents are combined into a context

A Fake LLM generates an answer

Question, answer, and related documents are stored in history

The Fake LLM is intentionally used to remove external API dependencies and simplify testing.
```
Client
  ↓
Django REST API
  ↓
PostgreSQL Full-Text Search
  ↓
Top-K Documents
  ↓
FakeLLM
  ↓
Response + History Storage
```

Core Stack

Python

Django

Django REST Framework

PostgreSQL

PostgreSQL Full-Text Search (SearchVector, SearchRank)

Jazmin (Custom Admin UI)

📦 Features

Semantic document retrieval using PostgreSQL FTS

Weighted ranking (title > content)

Top-K document selection for context control

Fake LLM for deterministic testing

Question/Answer history tracking

Custom styled admin panel (Jazmin)

Clean DRF-based API structure

```
project/
│
├── documents/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── search.py
│   ├── admin.py
│
├── DjangoProject3/
│
└── README.md
```
🧱 Data Models

```
| Field      | Type      | Description        |
| ---------- | --------- | ------------------ |
| title      | CharField | Unique title       |
| content    | TextField | Full text content  |
| tags       | CharField | Optional tags      |
| created_at | DateTime  | Creation timestamp |
| updated_at | DateTime  | Update timestamp   |

| Field        | Type      | Description                  |
| ------------ | --------- | ---------------------------- |
| question     | TextField | User input                   |
| answer       | TextField | LLM output                   |
| related_docs | JSONField | Retrieved documents snapshot |
| created_at   | DateTime  | Timestamp                    |
```

🔎 Retrieval Layer

The retrieval mechanism is built using:

SearchVector

SearchRank

GIN indexing (when enabled)

Why PostgreSQL FTS?

Database-level execution

Efficient ranking

Scalable for medium-sized datasets

No external ML dependencies

🤖 Fake LLM Layer

Instead of calling external APIs, a FakeLLM class is used.

Why?

Eliminates API token management

Removes network instability

Makes testing deterministic

Reduces cost

It can easily be replaced with:

HuggingFace

OpenAI

Any LangChain-compatible LLM

The architecture already supports that separation.

📁 Required Files

Dockerfile

docker-compose.yml

```
docker-compose up --build

docker-compose exec web python manage.py migrate

docker-compose exec web python manage.py createsuperuser

http://localhost:8000/search/

{
  "question": "کامپیوتر چیست"
}

http://localhost:8000/admin/


```

🎛 Admin Panel

Customized using Jazmin.

Provides:

Document management

QA history inspection

Retrieved document tracking

Administrative controls


<img width="1457" height="883" alt="Image" src="https://github.com/user-attachments/assets/4701b0f5-22c2-468c-ae17-191ab2aac228" />
<img width="1918" height="954" alt="Image" src="https://github.com/user-attachments/assets/7905b01f-1f90-42f2-a8eb-2d5fa3d5347f" />
<img width="1896" height="970" alt="Image" src="https://github.com/user-attachments/assets/c681ac0a-34c9-4a59-8041-f96be575e83b" />
<img width="1919" height="940" alt="Image" src="https://github.com/user-attachments/assets/c75f54e5-4a03-46b3-9f78-6d6c3a6a5e02" />
<img width="1588" height="845" alt="Image" src="https://github.com/user-attachments/assets/bff46ff7-b9c6-4ef8-845e-39b13ca36685" />
