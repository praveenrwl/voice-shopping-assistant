import requests
import json
import os
import re

OLLAMA_URL = "http://localhost:11434/api/generate"
headers = {"Content-Type": "application/json"}

# Load and filter product catalog based on user profile
def load_products(user_profile=None):
    file_path = os.path.join("data", "products.json")
    with open(file_path, "r", encoding="utf-8") as f:
        products = json.load(f)

    if not user_profile:
        return products

    age = user_profile.get("age", 10)
    interests = set(user_profile.get("interests", []))

    # Filter by age and tag match
    filtered = [
        p for p in products
        if age >= p.get("age_range", [0, 100])[0]
        and age <= p.get("age_range", [0, 100])[1]
        and interests.intersection(p.get("tags", []))
    ]
    return filtered

def format_product_context(filtered_products):
    return "\n".join(
        f"- {p['name']}: {p['description']} (₹{p['price']})"
        for p in filtered_products
    )


def clean_response(text: str) -> str:
    # Remove common unwanted patterns
    text = re.sub(r'^(Of course|Sure|Based on|I (would|recommend)).*?(?=\bTry\b|\bThe\b|\bBuy\b|\bCheck out\b)', '', text, flags=re.IGNORECASE)
    text = re.sub(r'(?i)based on.*?\b(query|question)\b[.,]?\s*', '', text)
    return text.strip()

def get_response(message: str, user_profile=None) -> str:
    filtered_products = load_products(user_profile)
    product_text = format_product_context(filtered_products)

    prompt = f"""
    From the catalog below, suggest the best product(s) that match the user's query. Be concise. Do not explain yourself. Respond in plain natural English. Don't say things like "Based on your query" or "I would recommend".

    CATALOG:
    {product_text}

    QUERY: {message}

    RECOMMENDATION:
    """

    payload = {
        "model": "llama2",
        "prompt": prompt,
        "stream": False
    }


    try:
        response = requests.post(OLLAMA_URL, headers=headers, json=payload)
        if response.status_code == 200:
            raw_reply = response.json().get("response", "Sorry, I didn’t get that.")
            return clean_response(raw_reply)
        else:
            return f"Error: {response.status_code}"
    except Exception as e:
        return f"Ollama Error: {str(e)}"
