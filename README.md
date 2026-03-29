# AI Lie Detector

## Overview

AI Lie Detector is a full-stack application that analyzes user-provided statements and determines whether they are likely true or false. The system combines machine learning and large language models to evaluate both linguistic patterns and factual correctness, and then produces a final verdict with a clear explanation.

The project demonstrates a hybrid AI architecture integrating a fine-tuned transformer model, a local LLM, and a decision engine, exposed through a FastAPI backend and an interactive React frontend.

---

## Features

* Detects whether a statement is true or false
* Differentiates between objective, personal, and opinion-based statements
* Uses a hybrid AI pipeline (ML + LLM)
* Provides a final verdict with a concise explanation
* Interactive UI with visual feedback (dual indicator bulbs)
* Real-time inference using a locally running LLM

---

## Tech Stack

### Frontend

* React (Vite)
* CSS (custom styling)

### Backend

* FastAPI
* Uvicorn

### Machine Learning / AI

* DistilBERT (fine-tuned for deception detection)
* Ollama (for running local LLM)
* LLaMA3 (LLM for reasoning and classification)

### Other Tools

* PyTorch
* Hugging Face Transformers

---

## Dataset Used

The model is trained on the **LIAR dataset**, which contains labeled political statements categorized into multiple truthfulness levels.

For this project:

* Labels were simplified into binary classes:

  * True (half-true, mostly-true, true)
  * False (pants-fire, false, barely-true)

This dataset enables the model to learn linguistic patterns associated with deceptive or truthful statements.

---

## How It Works

1. The user inputs a statement through the frontend.
2. The request is sent to the FastAPI backend.
3. The backend processes the statement through the AI pipeline:

   * DistilBERT analyzes linguistic deception patterns.
   * LLaMA3 (via Ollama) classifies the statement and provides a base verdict.
4. A decision engine combines both outputs to determine the final verdict:

   * Objective statements rely on LLM reasoning.
   * Personal and opinion statements rely on ML signals.
5. A final explanation is generated based on the final verdict.
6. The result is returned to the frontend and displayed visually.

---

## Project Structure

```
ai_lie_detector/
│
├── app.py                 # FastAPI backend
├── model/                 # Saved BERT model and tokenizer
├── src/
│   ├── predict.py         # Core AI pipeline
│   ├── fact_check.py      # LLM interaction logic
│
└── frontend/              # React application
```

---

## Setup Instructions

### 1. Clone the Repository

```
git clone https://github.com/your-username/ai-lie-detector.git
cd ai-lie-detector
```

---

### 2. Backend Setup

Install dependencies:

```
pip install fastapi uvicorn torch transformers ollama
```

---

### 3. Install and Setup Ollama

#### Install Ollama (Mac/Linux)

```
brew install ollama
```

Or download from the official site:
https://ollama.com

---

#### Start Ollama Server

```
ollama serve
```

---

#### Pull Required Model

```
ollama pull llama3
```

This will download the LLaMA3 model locally.

---

### 4. Run Backend Server

```
uvicorn app:app --reload
```

API will be available at:

```
http://127.0.0.1:8000
```

Swagger documentation:

```
http://127.0.0.1:8000/docs
```

---

### 5. Frontend Setup

Navigate to frontend:

```
cd frontend
npm install
npm run dev
```

Open in browser:

```
http://localhost:5173
```

---

## API Endpoint

### POST /predict

Request:

```
{
  "text": "Your statement here"
}
```

Response:

```
{
  "statement": "...",
  "type": "...",
  "confidence": 82.3,
  "verdict": "True",
  "reason": "..."
}
```

---

## Future Improvements

* Video-based lie detection using speech and facial analysis
* Support for external knowledge retrieval
* Database integration for history tracking
* Multi-language support
* Cloud deployment and scaling

---

## License

This project is made by Mayank Dhingra.
