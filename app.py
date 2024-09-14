from flask import Flask, request, jsonify
import time
import threading
from db import increment_user_requests
from models import rag_search
from caching import (
    get_user_request_count,
    increment_user_request_count,
    cache_search_result,
    get_cached_result,
)
from background_scraper import scrape_news

app = Flask(__name__)


@app.route("/search", methods=["POST"])
def search():
    start_time = time.time()
    data = request.json

    user_id = data.get("user_id")
    query_text = data.get("text", "")
    top_k = data.get("top_k", 5)
    threshold = data.get("threshold", 0.1)

    if not user_id or not query_text:
        return jsonify({"error": "user_id and text fields are required."}), 400

    increment_user_requests(user_id)

    if not increment_user_request_count(user_id):
        return jsonify({"error": "Rate limit exceeded. Please try again later."}), 429

    cache_key = f"rag_search_{user_id}_{query_text}_{top_k}_{threshold}"
    cached_result = get_cached_result(cache_key)

    if cached_result:
        results = cached_result
    else:

        results = rag_search(query_text, top_k)
        cache_search_result(cache_key, results)

    inference_time = time.time() - start_time

    return jsonify({"results": results, "inference_time": f"{inference_time:.2f}ms"})


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "API is active!"})


if __name__ == "__main__":
    # Start the scraping thread
    threading.Thread(target=scrape_news, daemon=True).start()
    app.run(debug=True)
