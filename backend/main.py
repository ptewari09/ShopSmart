from flask import Flask, request, jsonify
from serpapi import GoogleSearch
import json
import re

app = Flask(__name__)

@app.route('/search', methods=['POST'])
def search_products():
    data = request.get_json()  # Get data from the frontend
    query = data['query']
    min_price = data['min_price']
    max_price = data['max_price']

    # SerpAPI call to fetch results
    params = {
        "engine": "google_shopping",
        "q": query,
        "api_key": "ccc295b07cb8b5d0d6493c8a5cb9813e9ca93c06771722a4b751bf2d7a199fc0",
        "tbm": "shop"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    shopping_results = results["shopping_results"]

    # Filter products by price range
    filtered_products = []
    for product in shopping_results:
        price = product.get("price")
        price_match = re.search(r'[\d,.]+', price)
        price_value = float(price_match.group().replace(',', '')) if price_match else 0.0

        if min_price <= price_value <= max_price:
            filtered_products.append({
                "title": product.get("title"),
                "price": price,
                "link": product.get("link"),
                "image": product.get("thumbnail")
            })

    # Save results to JSON
    with open('api_results.json', 'w') as json_file:
        json.dump(filtered_products, json_file, indent=4)

    # Return results to frontend
    return jsonify(filtered_products)

if __name__ == '__main__':
    app.run(debug=True)
