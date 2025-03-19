from fastapi import FastAPI, HTTPException
import pandas as pd
import google.generativeai as genai
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json
import time

app = FastAPI()

# Load hotel booking dataset
csv_path = "hotel_bookings.csv"
df = pd.read_csv(csv_path) if csv_path else None

# Configure Gemini API
genai.configure(api_key="Your Gemini-API")
model_gemini = genai.GenerativeModel("gemini-2.0-flash")

# Load embedding model
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# Load FAISS index
faiss_index_path = "faiss_index.bin"
index = faiss.read_index(faiss_index_path)

# Root endpoint
@app.get("/")
def home():
    return {"message": "FastAPI is running. Use /analytics for reports and /ask for Q&A."}

# --- 📊 Analytics Endpoint ---
@app.post("/analytics")
def analytics():
    try:
        if df is None:
            raise HTTPException(status_code=500, detail="Dataset not loaded.")

        # Example analytics
        analytics_report = {
            "total_bookings": len(df),
            "unique_hotels": df["hotel"].nunique() if "hotel" in df.columns else "N/A",
            "average_price": df["price"].mean() if "price" in df.columns else "N/A",
            "most_popular_hotel": df["hotel"].mode()[0] if "hotel" in df.columns else "N/A",
        }

        return {"analytics": analytics_report}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- 🤖 Q&A Endpoint ---
@app.post("/ask")
def ask(query: str, k: int = 5):
    try:
        start_time = time.time()

        # Convert query to embedding
        query_embedding = np.array(embed_model.encode([query])).astype("float32")

        # Retrieve top k matches
        _, indices = index.search(query_embedding, k)

        # Extract relevant rows
        relevant_data = [df.iloc[i].to_dict() for i in indices[0] if i < len(df)]

        # Prepare query for Gemini
        prompt = f"Using this data {json.dumps(relevant_data)}, answer: {query}"
        response = model_gemini.generate_content(prompt)

        # Measure response time
        response_time = time.time() - start_time

        return {
            "answer": response.text,
            "response_time": round(response_time, 4)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
