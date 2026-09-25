# 🤖 AI Research Multi-Agent System

A multi-agent AI research system that searches the web, reads relevant sources, generates a structured research report, and critiques the final report.

The system is exposed through a **FastAPI backend** and uses background jobs so that long-running research tasks do not block the API request.

---

## 📌 Overview

This project demonstrates how multiple AI agents and LLM components can work together to automate a research workflow.

Given a research topic, the system:

1. Searches the web for recent and relevant information.
2. Selects and reads a relevant source.
3. Generates a structured research report.
4. Reviews the generated report using a critic.
5. Returns the result through a FastAPI API.

The research pipeline runs as a background task, allowing the API to return a `job_id` immediately while the research continues in the background.

---

## ✨ Features

* 🔎 **Web Search Agent** using Tavily
* 🌐 **Reader Agent** for extracting content from web pages
* ✍️ **AI Research Writer** for generating structured reports
* 🔍 **Critic Agent** for reviewing generated reports
* ⚡ **FastAPI REST API**
* 🔄 **Background job processing** for long-running research
* 📊 **Job status tracking**
* ✅ **Pydantic request and response validation**
* ⚠️ **HTTP error handling**
* 🎯 **LLM output token control**
* 📖 Interactive API documentation with Swagger UI

---

## 🏗️ Architecture

```text
                    Client
                      │
                      ▼
              ┌───────────────┐
              │    FastAPI    │
              └───────┬───────┘
                      │
                POST /research
                      │
                      ▼
                Generate Job ID
                      │
                      ▼
              Background Job
                      │
                      ▼
             Research Pipeline
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
   Search Agent   Reader Agent    Writer
        │             │             │
     Tavily       Web Scraper      LLM
        │             │             │
        └─────────────┼─────────────┘
                      │
                      ▼
                   Critic
                      │
                      ▼
                 Final Result
                      │
                      ▼
          GET /research/{job_id}/report
```

---

## 🔄 Research Workflow

### Step 1 — Search Agent

The search agent uses Tavily to find relevant web sources.

It collects:

* Source titles
* URLs
* Search snippets

### Step 2 — Reader Agent

The reader agent examines the search results and selects a relevant URL.

The URL is passed to a scraping tool that extracts readable page content.

### Step 3 — Writer

The writer receives the search results and scraped content and generates a structured research report containing:

* Introduction
* Key findings
* Conclusion
* Sources

### Step 4 — Critic

The critic reviews the generated report and provides:

* Score
* Strengths
* Areas to improve
* Final verdict

---

## 🛠️ Tech Stack

| Technology    | Purpose                     |
| ------------- | --------------------------- |
| Python        | Core programming language   |
| FastAPI       | API/backend framework       |
| LangChain     | Agent and LLM orchestration |
| Groq          | LLM inference               |
| Tavily        | Web search                  |
| BeautifulSoup | Web scraping                |
| Requests      | HTTP requests               |
| Pydantic      | Data validation             |
| Uvicorn       | ASGI server                 |

### Model

The project currently uses:

```text
openai/gpt-oss-20b
```

through the Groq API.

---

## 📁 Project Structure

```text
AI-Research-Project/
│
├── main.py
├── agents.py
├── tools.py
├── pipeline.py
├── schemas.py
├── .env
├── .gitignore
├── README.md
└── requirements.txt
```

> `.env` should remain local and must never be committed to GitHub.

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd AI-Research-Project
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Never commit your actual API keys.

---

## ▶️ Running the API

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

## 🔌 API Endpoints

### Start Research

```http
POST /research
```

Request:

```json
{
  "topic": "Impact of artificial intelligence on healthcare"
}
```

Response:

```json
{
  "job_id": "example-job-id",
  "status": "queued",
  "message": "Research started"
}
```

The API returns immediately while the research continues in the background.

---

### Check Job Status

```http
GET /research/{job_id}/status
```

Example response:

```json
{
  "job_id": "example-job-id",
  "status": "completed",
  "topic": "Impact of artificial intelligence on healthcare"
}
```

Possible states include:

```text
queued
running
completed
failed
```

---

### Get Research Report

```http
GET /research/{job_id}/report
```

Example response:

```json
{
  "job_id": "example-job-id",
  "status": "completed",
  "topic": "Impact of artificial intelligence on healthcare",
  "report": "Generated research report...",
  "feedback": "Critic feedback..."
}
```

---

## ⚡ Background Job Flow

Research can take significantly longer than a normal API request because multiple AI operations are performed.

Instead of keeping the HTTP request waiting:

```text
Client
  │
  │ POST /research
  ▼
FastAPI
  │
  ├── Creates job_id
  │
  └── Starts background task
          │
          ▼
    Research Pipeline
```

The client can then check the status:

```text
GET /research/{job_id}/status
```

and retrieve the final report after completion:

```text
GET /research/{job_id}/report
```

---

## 🧠 Why This Architecture?

The project separates the API layer from the AI research workflow.

```text
main.py
   ↓
API layer

pipeline.py
   ↓
Research workflow

agents.py
   ↓
AI agents and LLM chains

tools.py
   ↓
External tools

schemas.py
   ↓
API data validation
```

This separation makes the application easier to understand, maintain, and extend.

---

## ⚠️ Current Limitations

This project is designed as a portfolio and learning project.

The current background-job implementation uses an in-memory Python dictionary to store job information.

Therefore:

* Jobs are lost when the server restarts.
* Job data is not persistent.
* It is not designed for multiple server instances.
* The background task system is not a full distributed task queue.

---

## 🚀 Future Improvements

Possible future improvements include:

* Redis for persistent job state
* Celery/RQ or another worker system for distributed background processing
* Database-backed research history
* User authentication
* Frontend interface
* Docker deployment
* Better source verification
* More specialized research agents
* Persistent report storage

---

## 🎯 Project Goal

The goal of this project was to explore how **LLMs, agents, tools, and APIs can be combined to build a practical AI application**.

It demonstrates the complete flow from:

```text
User Topic
    ↓
Web Research
    ↓
Source Reading
    ↓
AI Report Generation
    ↓
AI Criticism
    ↓
FastAPI
    ↓
Final Research Report
```

---


