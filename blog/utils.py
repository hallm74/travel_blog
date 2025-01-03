import openai
import requests

def generate_blog_content(title, api_key, prompt_template=None):
    """
    Use OpenAI to generate blog content based on the title.
    """
    if not title:
        raise ValueError("Title cannot be empty.")

    openai.api_key = api_key
    prompt = prompt_template or f"Write a detailed blog post about {title}. Include an introduction, main points, and a conclusion."
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a professional travel blogger."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        # Log the error for debugging
        print(f"Error generating blog content: {e}")
        raise RuntimeError(f"Error generating content: {e}")

def fetch_unsplash_image(query, api_key, per_page=1):
    """
    Fetch an image URL from Unsplash based on the query.
    """
    if not query:
        raise ValueError("Query cannot be empty.")

    url = "https://api.unsplash.com/search/photos"
    headers = {"Authorization": f"Client-ID {api_key}"}
    params = {"query": query, "per_page": per_page}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data['results']:
            # Return the first result or a list based on per_page
            if per_page == 1:
                return data['results'][0]['urls']['regular']
            else:
                return [result['urls']['regular'] for result in data['results']]
        else:
            raise RuntimeError(f"No images found for query: {query}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching image for query '{query}': {e}")
        raise RuntimeError(f"Error fetching image: {e}")

def extract_location_from_content(content):
    """
    Use ChatGPT to dynamically extract the location from the generated content.
    """
    location = ask_chatgpt_for_location(content)
    return location

def ask_chatgpt_for_location(content):
    """
    Ask ChatGPT to identify the location from the generated content.
    """
    prompt = f"Please extract the main location mentioned in the following text:\n\n{content}\n\nLocation:"
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Or your preferred model
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ]
    )
    location = response['choices'][0]['message']['content']
    return location.strip()