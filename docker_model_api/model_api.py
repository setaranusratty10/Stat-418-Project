# model_api.py

from flask import Flask, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)

# Load data and model
df = pd.read_csv("data.csv")
model = joblib.load("book_knn_model.pkl")

# Recommendation function
def recommend(title, k=10, min_rating=0.0, max_pages=10000):
    idx = df.index[df["title"].str.lower() == title.lower()]
    if idx.empty:
        return []
    vec = model["prep"].transform(df.iloc[[idx[0]]])
    _, ix = model["knn"].kneighbors(vec, n_neighbors=k + 1)
    recs = df.iloc[ix[0][1:]]
    recs = recs.query("avg_rating >= @min_rating and num_pages <= @max_pages")
    return recs[["title", "author", "avg_rating", "url"]].to_dict(orient="records")

@app.route("/recommend", methods=["POST"])
def recommend_route():
    data = request.json
    title = data.get("title")
    k = int(data.get("k", 10))
    min_rating = float(data.get("min_rating", 0.0))
    max_pages = int(data.get("max_pages", 10000))
    results = recommend(title, k, min_rating, max_pages)
    return jsonify(results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)