from django.core.management.base import BaseCommand
import os
import re
import openai
import requests
from decouple import config


def sanitize_text(text):
    """
    Remove colons and other restricted characters from text and strip leading 'Title'.
    """
    text = text.replace(":", "-")
    text = re.sub(r"^[Tt]itle[-:]?\s*", "", text)  # Remove 'Title' at the start
    return re.sub(r"[^\w\s\-,.]", "", text).strip()


def extract_description(content, word_limit=25):
    """
    Extract the description from the main body of the content.
    Use the first `word_limit` words as the description.
    """
    content = re.sub(r"^[Tt]itle[-:]?\s*", "", content.strip())  # Remove 'Title' at the start
    words = re.split(r'\s+', content)  # Split content into words
    description = " ".join(words[:word_limit])  # Take the first `word_limit` words
    return sanitize_text(description)


def save_post(title, content, image_url, folder="generated_posts"):
    """
    Save the blog post content and image URL as a Markdown file.
    """
    os.makedirs(folder, exist_ok=True)

    # Clean up the description and main content
    description = extract_description(content)
    content = re.sub(r"^[Tt]itle[-:]?\s*", "", content.strip(), flags=re.MULTILINE)

    filename = os.path.join(folder, f"{sanitize_text(title).replace(' ', '_').lower()}.md")
    with open(filename, "w") as file:
        file.write(f"---\n")
        file.write(f"title: \"{sanitize_text(title)}\"\n")
        file.write(f"description: \"{description}\"\n")
        file.write(f"pubDatetime: 2025-01-02T12:00:00\n")
        file.write(f"tags:\n  - travel\n  - culture\n  - adventure\n")
        file.write(f"ogImage: {image_url}\n")
        file.write(f"draft: false\n")
        file.write(f"---\n\n")
        file.write(f"![Cover Image]({image_url})\n\n")
        file.write(content)
    return filename


def generate_blog_content(topic):
    """
    Use ChatGPT to generate blog content for a given topic.
    """
    openai.api_key = config('CHATGPT_API_KEY')
    prompt = f"Write a detailed blog post about {topic}. Include a catchy introduction and key points."
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a professional travel blogger."},
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content']


def fetch_unsplash_image(query):
    """
    Fetch a relevant image from Unsplash for the given query.
    """
    unsplash_api_key = config('UNSPLASH_API_KEY')
    url = "https://api.unsplash.com/search/photos"
    headers = {"Authorization": f"Client-ID {unsplash_api_key}"}
    params = {"query": query, "per_page": 1}

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    if data['results']:
        return data['results'][0]['urls']['regular']
    return None


class Command(BaseCommand):
    help = "Generate Astro-compatible blog posts using ChatGPT and Unsplash."

    def add_arguments(self, parser):
        parser.add_argument("--title", type=str, help="The title for the blog post.")

    def handle(self, *args, **options):
        title = options["title"]

        if not title:
            self.stderr.write("Please provide a title using --title.")
            return

        self.process_post(title)

    def process_post(self, title):
        """
        Generate a single blog post.
        """
        try:
            content = generate_blog_content(title)
            image_url = fetch_unsplash_image(title)

            file_path = save_post(title, content, image_url)
            self.stdout.write(f"Post saved successfully at: {file_path}")
        except Exception as e:
            self.stderr.write(f"Failed to process post '{title}': {e}")