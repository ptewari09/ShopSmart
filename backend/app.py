from flask import Flask, jsonify, request
from main import send_query, filter_products, save_results_to_json
import os
import json

app = Flask(__name__)

# Ensure data folder exists
os.makedirs("data", exist_ok=True)

# Home route
@app.route("/")
def home():
    return "Welcome to ShopSmart!"

# Route to trigger search and filtering (via POST from frontend)
@app.route("/products", methods=["POST"])
def get_products():
    data = request.get_json()
    search_query = data.get("searchQuery")
    min_price = int(data.get("minPrice", 0))
    max_price = int(data.get("maxPrice", 1000000))

    if not search_query:
        return jsonify({"error": "Missing required parameter 'searchQuery'"}), 400

    # Fetch results from SerpAPI
    results = send_query(search_query)
    filtered = filter_products(results, max_price)

    # Save filtered data to file
    save_results_to_json(filtered)

    return jsonify({"status": "success", "count": len(filtered)})

# Route to fetch saved product data (GET request)
@app.route("/products", methods=["GET"])
def display_saved_products():
    try:
        with open("data/api_results.json", encoding="utf-8") as json_file:
            parsed_json = json.load(json_file)
        return jsonify(parsed_json)
    except FileNotFoundError:
        return jsonify({"error": "No product data found. Please make a POST request first."}), 404

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
