from django.contrib import admin
from django.utils.html import format_html
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

@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basic Info',  {'fields': ('name', 'tagline', 'description', 'logo')}),
        ('Contact',     {'fields': ('email', 'phone', 'address')}),
        ('Social',      {'fields': ('linkedin_url', 'twitter_url', 'github_url', 'instagram_url')}),
        ('Stats',       {'fields': ('projects_count', 'clients_count', 'years_experience')}),
    )


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display  = ['name', 'role', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter   = ['is_active']


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display  = ['name', 'email', 'subject', 'submitted_at', 'is_read']
    list_filter   = ['is_read', 'submitted_at']
    list_editable = ['is_read']
    readonly_fields = ['name', 'email', 'phone', 'company', 'subject', 'message', 'submitted_at']
    search_fields = ['name', 'email', 'subject']

    def has_add_permission(self, request):
        return False  # submissions come from the contact form only


# ─────────────────────────────────────────────
# CLIENTS & TESTIMONIALS
# ─────────────────────────────────────────────

class TestimonialInline(admin.TabularInline):
    model  = Testimonial
    extra  = 0
    fields = ['author_name', 'author_role', 'content', 'rating', 'is_featured', 'is_approved']


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display  = ['name', 'logo_preview', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['name']
    inlines       = [TestimonialInline]

    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" height="40" />', obj.logo.url)
        return '—'
    logo_preview.short_description = 'Logo'


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display  = ['author_name', 'author_role', 'client', 'rating', 'is_featured', 'is_approved']
    list_editable = ['is_featured', 'is_approved']
    list_filter   = ['is_featured', 'is_approved', 'rating']


# ─────────────────────────────────────────────
# SERVICES
# ─────────────────────────────────────────────

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display  = ['title', 'slug', 'order', 'is_active', 'is_featured']
    list_editable = ['order', 'is_active', 'is_featured']
    prepopulated_fields = {'slug': ('title',)}


# ─────────────────────────────────────────────
# PROJECTS
# ─────────────────────────────────────────────

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display  = ['title', 'category', 'client', 'is_published', 'is_featured', 'start_date']
    list_editable = ['is_published', 'is_featured']
    list_filter   = ['category', 'is_published', 'is_featured']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    autocomplete_fields = ['client']


# ─────────────────────────────────────────────
# BLOG
# ─────────────────────────────────────────────

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display  = ['title', 'category', 'author', 'is_published', 'is_featured', 'created_at']
    list_editable = ['is_published', 'is_featured']
    list_filter   = ['is_published', 'is_featured', 'category', 'created_at']
    search_fields = ['title', 'excerpt', 'content']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal   = ['tags']
    fieldsets = (
        ('Content',   {'fields': ('title', 'slug', 'category', 'tags', 'author', 'author_photo', 'cover_image')}),
        ('Body',      {'fields': ('excerpt', 'content')}),
        ('Settings',  {'fields': ('is_published', 'is_featured')}),
    )
