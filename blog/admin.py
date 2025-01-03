from django.contrib import admin
from .models import BlogPost, Tag
from django.utils.html import format_html

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'pub_date', 'draft_status', 'get_image_url')
    list_filter = ('pub_date', 'author', 'tags')
    search_fields = ('title', 'content', 'description')
    actions = ['generate_content_and_image_action']

    # Define a custom method to display the image as a thumbnail in the admin
    def get_image_url(self, obj):
        if obj.image_url:
            return format_html('<img src="{}" style="width: 50px; height: auto;" />', obj.image_url)
        return "No Image"
    get_image_url.short_description = 'Image'

    # Display draft status based on content existence
    def draft_status(self, obj):
        return "Draft" if not obj.content else "Published"
    draft_status.short_description = "Status"

    def save_model(self, request, obj, form, change):
        """
        Override the save_model method to automatically generate content, description, and image
        when saving a BlogPost from the admin.
        """
        if not obj.content:
            obj.generate_content_and_image()  # This will trigger content generation
        super().save_model(request, obj, form, change)

    # Admin action to generate content and fetch image
    @admin.action(description="Generate content and fetch image")
    def generate_content_and_image_action(self, request, queryset):
        """
        Admin action to generate content and fetch images for selected blog posts.
        """
        for post in queryset:
            try:
                post.generate_content_and_image()  # Trigger content generation and image fetching
                post.save()  # Save after generating content
                self.message_user(request, f"Content and image generated for '{post.title}' successfully.")
            except Exception as e:
                self.message_user(request, f"Failed for '{post.title}': {e}", level="error")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)