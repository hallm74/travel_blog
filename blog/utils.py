import openai
import requests

# Function to generate blog content using ChatGPT
def generate_blog_content(topic, chatgpt_api_key):
    openai.api_key = chatgpt_api_key
    try:
        prompt = f"Write a detailed blog post about {topic}. Include a catchy title and a short introduction. Provide at least three key points and a conclusion."
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a professional travel blogger."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        raise ValueError(f"ChatGPT Error: {e}")

# Function to fetch an image from Unsplash
def fetch_unsplash_image(query, unsplash_api_key):
    url = "https://api.unsplash.com/search/photos"
    headers = {"Authorization": f"Client-ID {unsplash_api_key}"}
    params = {"query": query, "per_page": 1}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        data = response.json()
        if data['results']:
            return data['results'][0]['urls']['regular']
        return None
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Unsplash API Error: {e}")