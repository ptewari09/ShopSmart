from serpapi import GoogleSearch
import json
import re
import os

def search_prod(query):
    params = {
        "engine": "google_shopping",
        "q": query,
        "api_key": "e71a0c7217eca0d5e490c9db2feca84a47253ce6b3a0d19195eaabd2a888d488",  # Replace with your actual API key
        "tbm": "shop",
        "gl": "in"
    }
    search = GoogleSearch(params)
    result = search.get_dict()
    print("API response:", result)  # Check the full response from the API
    return result

def send_query(query):
    print("Received query:", query)
    results = search_prod(query)
    return results.get("shopping_results", [])

def filter_products(results, max_price):
    print("Filtering products below ₹", max_price)
    filtered = []

    for product in results:
        title = product.get("title")
        price = product.get("price")
        print(f"Product: {title}")
        print(f"Raw Price: {price}")

        link = product.get("product_link")
        seller = product.get("source")

        # Parse numeric price
        price_val = 0.0
        if isinstance(price, str):
            # Extract all prices in case it's a range
            matches = re.findall(r'[\d,]+', price)
            if matches:
                price_val = float(matches[0].replace(",", ""))  # Use the *lowest* price

        print(f"Parsed Price: {price_val}")
        if price_val <= max_price:
            print("✅ Added")
            filtered.append({
                "title": title,
                "price": price,
                "link": link,
                "seller": seller
            })
        else:
            print("❌ Skipped, too expensive.")

    if not filtered:
        print("No products found within the price range.")
    return filtered

def save_results_to_json(data):
    os.makedirs('data', exist_ok=True)  # Ensure 'data' folder exists
    with open('data/api_results.json', 'w', encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def main():
    # Define the products and their max prices to search for
    query = {
        "iphone 15": 70000.00,  # Max price for iPhone 15
        "apple watch series 9": 40000.00  # Max price for Apple Watch Series 9
    }

    # Iterate through each product to search and filter results
    for product, max_price in query.items():
        results = send_query(product)  # Search for the product
        filtered_products = filter_products(results, max_price)  # Filter based on max price
        if filtered_products:  # If there are filtered products
            save_results_to_json(filtered_products)  # Save them to JSON file
            print(f"Results saved for {product}")
        else:
            print(f"No products found for {product}")

if __name__ == "__main__":
    main()

