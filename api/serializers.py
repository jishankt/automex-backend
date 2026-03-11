from rest_framework import serializers
from .models import (
    CompanyInfo, TeamMember, ContactSubmission,
    Client, Testimonial,
    Service,
    Project,
    Category, Tag, Post,
)


# ─────────────────────────────────────────────
# COMPANY
# ─────────────────────────────────────────────

class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model  = TeamMember
        fields = ['id', 'name', 'role', 'bio', 'photo', 'linkedin', 'twitter', 'github', 'order']


class CompanyInfoSerializer(serializers.ModelSerializer):
    team_members = TeamMemberSerializer(many=True, read_only=True, source='teammember_set')

    class Meta:
        model  = CompanyInfo
        fields = [
            'id', 'name', 'tagline', 'description', 'email', 'phone', 'address', 'logo',
            'linkedin_url', 'twitter_url', 'github_url', 'instagram_url',
            'projects_count', 'clients_count', 'years_experience',
            'team_members',
        ]


class ContactSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ContactSubmission
        fields = ['id', 'name', 'email', 'phone', 'company', 'subject', 'message', 'submitted_at']
        read_only_fields = ['submitted_at']


# ─────────────────────────────────────────────
# CLIENTS & TESTIMONIALS
# ─────────────────────────────────────────────

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Testimonial
        fields = ['id', 'author_name', 'author_role', 'author_photo', 'content', 'rating', 'is_featured']


class ClientSerializer(serializers.ModelSerializer):
    testimonials = TestimonialSerializer(many=True, read_only=True)

    class Meta:
        model  = Client
        fields = ['id', 'name', 'logo', 'website', 'description', 'order', 'testimonials']


# ─────────────────────────────────────────────
# SERVICES
# ─────────────────────────────────────────────

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Service
        fields = ['id', 'title', 'slug', 'short_desc', 'description', 'icon', 'image', 'order', 'is_featured']


# ─────────────────────────────────────────────
# PROJECTS
# ─────────────────────────────────────────────

class ProjectSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    tech_list        = serializers.ListField(read_only=True)
    client_name      = serializers.CharField(source='client.name', read_only=True)

    class Meta:
        model  = Project
        fields = [
            'id', 'title', 'slug', 'category', 'category_display',
            'client_name', 'short_desc', 'description', 'image',
            'tech_stack', 'tech_list', 'live_url', 'github_url',
            'start_date', 'end_date', 'is_featured', 'created_at',
        ]


# ─────────────────────────────────────────────
# BLOG
# ─────────────────────────────────────────────

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Tag
        fields = ['id', 'name', 'slug']


class CategorySerializer(serializers.ModelSerializer):
    post_count = serializers.IntegerField(source='posts.count', read_only=True)

    class Meta:
        model  = Category
        fields = ['id', 'name', 'slug', 'description', 'post_count']


class PostListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views."""
    category = CategorySerializer(read_only=True)
    tags     = TagSerializer(many=True, read_only=True)

    class Meta:
        model  = Post
        fields = [
            'id', 'title', 'slug', 'category', 'tags',
            'author', 'author_photo', 'excerpt', 'cover_image',
            'is_featured', 'created_at',
        ]


class PostDetailSerializer(PostListSerializer):
    """Full serializer for detail views – includes content."""
    class Meta(PostListSerializer.Meta):
        fields = PostListSerializer.Meta.fields + ['content', 'updated_at']
