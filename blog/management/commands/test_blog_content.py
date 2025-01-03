from django.core.management.base import BaseCommand
from blog.models import BlogPost, Tag
from blog.utils import generate_blog_content, fetch_unsplash_image
from decouple import config
import re

class Command(BaseCommand):
    help = "Test content generation, Unsplash image fetching, and tag association for BlogPost."

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Starting test for BlogPost content generation..."))

        # Test data
        test_title = "Exploring the Vibrant Culture of New Orleans"
        chatgpt_api_key = config("CHATGPT_API_KEY")
        unsplash_api_key = config("UNSPLASH_API_KEY")

        try:
            # Test content generation
            self.stdout.write(f"Generating content for: {test_title}")
            content = generate_blog_content(test_title, chatgpt_api_key)

            # Remove "Title:" from the generated content using regex
            content = re.sub(r"^\s*Title:\s*", "", content).strip()

            self.stdout.write(self.style.SUCCESS("Content generated successfully:"))
            self.stdout.write(content[:500] + "...")  # Display first 500 characters

            # Test image fetching
            self.stdout.write(f"Fetching image for: {test_title}")
            image_url = fetch_unsplash_image(test_title, unsplash_api_key)
            self.stdout.write(self.style.SUCCESS(f"Image URL fetched successfully: {image_url}"))

            # Save a test BlogPost instance
            self.stdout.write("Saving test BlogPost instance...")
            post = BlogPost.objects.create(
                title=test_title,
                content=content,
                description=" ".join(content.split()[:25])[:500],  # Truncate description to 500 characters
                image_url=image_url
            )

            # Generate and associate tags
            self.stdout.write("Generating tags for the BlogPost...")
            title_keywords = [word.lower() for word in test_title.split()]
            tag_names = list(set(title_keywords) & set(['travel', 'culture', 'adventure', 'food', 'exploration']))
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                post.tags.add(tag)

            post.save()
            self.stdout.write(self.style.SUCCESS(f"Test BlogPost saved with ID: {post.id}"))

            # Display associated tags
            self.stdout.write("Associated Tags:")
            for tag in post.tags.all():
                self.stdout.write(f"- {tag.name}")

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error during test: {e}"))