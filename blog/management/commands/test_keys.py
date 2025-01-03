import re
import os
from django.core.management.base import BaseCommand
from decouple import config
import openai
import requests


def sanitize_text(text):
    """
    Remove colons and other restricted characters from text.
    Args:
        text (str): The input text to sanitize.
    Returns:
        str: Sanitized text.
    """
    # Replace colons with dashes or spaces
    text = text.replace(":", "-")
    # Remove any other unwanted characters (e.g., special symbols)
    text = re.sub(r"[^\w\s\-,.]", "", text)
    return text.strip()


def extract_description(content):
    """
    Extract the description from the content.
    Use the first non-empty paragraph as the description.
    """
    paragraphs = content.split("\n")
    for paragraph in paragraphs:
        if paragraph.strip():  # Skip empty lines
            return sanitize_text(paragraph.strip())
    return "No description available."


def save_post(title, content, image_url, folder="generated_posts"):
    """
    Save the blog post content and image URL as a Markdown file.

    Args:
        title (str): Title of the post.
        content (str): Main body of the post.
        image_url (str): URL of the cover image.
        folder (str): Folder where the post will be saved.

    Returns:
        str: Path to the saved file.
    """
    # Ensure the folder exists
    os.makedirs(folder, exist_ok=True)

    # Sanitize title and description
    sanitized_title = sanitize_text(title)
    description = extract_description(content)

    # Create a filename based on the sanitized title
    filename = os.path.join(folder, f"{sanitized_title.replace(' ', '_').lower()}.md")
    
    # Write to the file
    with open(filename, "w") as file:
        # Frontmatter for Astro
        file.write(f"---\n")
        file.write(f"title: \"{sanitized_title}\"\n")
        file.write(f"description: \"{description}\"\n")
        file.write(f"pubDatetime: 2025-01-02T12:00:00\n")
        file.write(f"tags:\n  - travel\n  - Peru\n  - mountains\n")
        file.write(f"ogImage: {image_url}\n")
        file.write(f"draft: false\n")
        file.write(f"---\n\n")
        
        # Cover image and content
        file.write(f"![Cover Image]({image_url})\n\n")
        file.write(content)
    
    return filename


class Command(BaseCommand):
    help = "Test Unsplash and ChatGPT API keys and save a sample post"

    def handle(self, *args, **kwargs):
        # Load API keys
        chatgpt_api_key = config('CHATGPT_API_KEY')
        unsplash_api_key = config('UNSPLASH_API_KEY')

        # Test ChatGPT API
        try:
            prompt = "Write a detailed blog post about the mountains of Peru. Include a title, an introduction, key points, and a conclusion."
            openai.api_key = chatgpt_api_key
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a professional travel blogger."},
                    {"role": "user", "content": prompt}
                ]
            )
            content = response['choices'][0]['message']['content']
            self.stdout.write("ChatGPT Test Successful:\n" + content)
        except Exception as e:
            self.stderr.write(f"ChatGPT Test Failed: {e}")
            return

        # Test Unsplash API
        try:
            query = "mountains"
            url = "https://api.unsplash.com/search/photos"
            headers = {"Authorization": f"Client-ID {unsplash_api_key}"}
            params = {"query": query, "per_page": 1}

            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            data = response.json()
            if data['results']:
                image_url = data['results'][0]['urls']['regular']
                self.stdout.write(f"Unsplash Test Successful: Image URL - {image_url}")
            else:
                self.stderr.write("Unsplash Test Successful but no images found.")
                image_url = None
        except Exception as e:
            self.stderr.write(f"Unsplash Test Failed: {e}")
            return

        # Save the post if both tests were successful
        try:
            title = "Unearthing the Summits of the Andes: A Spirited Journey into Peru's Majestic Mountains"
            file_path = save_post(title, content, image_url)
            self.stdout.write(f"Post saved successfully at: {file_path}")
        except Exception as e:
            self.stderr.write(f"Failed to save post: {e}")