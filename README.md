# Hotel Booking Q&A API

## Overview
This project is a REST API built using **FastAPI** that provides:
1. **Booking Analytics**: Summarizes key booking insights.
2. **Q&A System**: Uses Google's **Gemini AI** and **FAISS vector search** to answer booking-related queries.

## Features
- **POST /analytics** → Returns booking analytics.
- **POST /ask** → Answers booking-related questions using FAISS and Gemini AI.
- **Precomputed FAISS Index** for fast retrieval.
- **Scalable & Lightweight** with FastAPI.

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/hotel-booking-api.git
cd hotel-booking-api
```

### 2. Install Dependencies
Make sure you have Python **3.8+** installed.
```bash
pip install -r requirements.txt
```

### 3. Get a Gemini API Key
- Visit [Google AI Studio](https://aistudio.google.com/) and generate an API key.
- Set up an environment variable:
  ```bash
  export GEMINI_API_KEY="your-api-key-here"
  ```
  Or replace `api_key` in `main.py` directly.

### 4. Prepare the Data & FAISS Index
- Ensure `hotel_bookings.csv` is in the project directory.
- If the FAISS index is not available, run:
  ```bash
  python generate_faiss_index.py
  ```

### 5. Run the API
```bash
uvicorn main:app --reload
```

## API Endpoints

### 1. Analytics Endpoint
**URL:** `/analytics`  
**Method:** `POST`  
**Description:** Returns summary analytics of hotel bookings.  
**Example Response:**
```json
{
  "total_revenue": 500000,
  "cancellation_rate": 12.5,
  "top_countries": {"USA": 200, "UK": 150},
  "lead_time_distribution": {"mean": 30, "std": 15}
}
```

### 2. Q&A Endpoint
**URL:** `/ask`  
**Method:** `POST`  
**Description:** Answers booking-related queries using FAISS + Gemini AI.  
**Request Body:**
```json
{
  "query": "What is the average booking price?",
  "k": 3
}
```
**Example Response:**
```json
{
  "answer": "The average booking price is $120 per night."
}
```

## Performance Evaluation
- **Response Accuracy**: Validate correctness of answers.
- **API Response Time**: Measure query execution speed.

## Deployment
- Deploy using Docker, AWS, or GCP.
- Example: Deploy with **Gunicorn** & **Uvicorn**:
  ```bash
  gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
  ```
---