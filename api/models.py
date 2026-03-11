from django.db import models
from django.utils.text import slugify


# ─────────────────────────────────────────────
# COMPANY / CORE
# ─────────────────────────────────────────────

class CompanyInfo(models.Model):
    name            = models.CharField(max_length=200, default="AutoMex")
    tagline         = models.CharField(max_length=300, blank=True)
    description     = models.TextField(blank=True)
    email           = models.EmailField(blank=True)
    phone           = models.CharField(max_length=20, blank=True)
    address         = models.TextField(blank=True)
    logo            = models.ImageField(upload_to='company/', blank=True, null=True)
    # Social
    linkedin_url    = models.URLField(blank=True)
    twitter_url     = models.URLField(blank=True)
    github_url      = models.URLField(blank=True)
    instagram_url   = models.URLField(blank=True)
    # Stats
    projects_count  = models.PositiveIntegerField(default=0)
    clients_count   = models.PositiveIntegerField(default=0)
    years_experience= models.PositiveIntegerField(default=0)
    # Meta
    updated_at      = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Company Info"
        verbose_name_plural = "Company Info"

    def __str__(self):
        return self.name


class TeamMember(models.Model):
    name        = models.CharField(max_length=200)
    role        = models.CharField(max_length=200)
    bio         = models.TextField(blank=True)
    photo       = models.ImageField(upload_to='team/', blank=True, null=True)
    linkedin    = models.URLField(blank=True)
    twitter     = models.URLField(blank=True)
    github      = models.URLField(blank=True)
    order       = models.PositiveIntegerField(default=0)
    is_active   = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.name} – {self.role}"


class ContactSubmission(models.Model):
    name         = models.CharField(max_length=200)
    email        = models.EmailField()
    phone        = models.CharField(max_length=20, blank=True)
    company      = models.CharField(max_length=200, blank=True)
    subject      = models.CharField(max_length=300)
    message      = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_read      = models.BooleanField(default=False)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.name} – {self.subject}"


# ─────────────────────────────────────────────
# CLIENTS & TESTIMONIALS
# ─────────────────────────────────────────────

class Client(models.Model):
    name        = models.CharField(max_length=200)
    logo        = models.ImageField(upload_to='clients/', blank=True, null=True)
    website     = models.URLField(blank=True)
    description = models.TextField(blank=True)
    order       = models.PositiveIntegerField(default=0)
    is_active   = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Testimonial(models.Model):
    client      = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True, related_name='testimonials')
    author_name = models.CharField(max_length=200)
    author_role = models.CharField(max_length=200, blank=True)
    author_photo= models.ImageField(upload_to='testimonials/', blank=True, null=True)
    content     = models.TextField()
    rating      = models.PositiveSmallIntegerField(default=5)
    is_featured = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.author_name} – {self.author_role}"


# ─────────────────────────────────────────────
# SERVICES
# ─────────────────────────────────────────────

class Service(models.Model):
    title       = models.CharField(max_length=200)
    slug        = models.SlugField(unique=True, blank=True)
    short_desc  = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    icon        = models.CharField(max_length=100, blank=True, help_text="CSS icon class or emoji")
    image       = models.ImageField(upload_to='services/', blank=True, null=True)
    order       = models.PositiveIntegerField(default=0)
    is_active   = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['order', 'title']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# ─────────────────────────────────────────────
# PROJECTS
# ─────────────────────────────────────────────

class Project(models.Model):
    PROJECT_CATEGORIES = [
        ('web',     'Web Development'),
        ('mobile',  'Mobile Development'),
        ('cloud',   'Cloud Solutions'),
        ('data',    'Data Analytics'),
        ('ai',      'AI / ML'),
        ('other',   'Other'),
    ]

    title           = models.CharField(max_length=200)
    slug            = models.SlugField(unique=True, blank=True)
    category        = models.CharField(max_length=50, choices=PROJECT_CATEGORIES, default='web')
    client          = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True, related_name='projects')
    short_desc      = models.CharField(max_length=300, blank=True)
    description     = models.TextField(blank=True)
    image           = models.ImageField(upload_to='projects/', blank=True, null=True)
    tech_stack      = models.CharField(max_length=500, blank=True, help_text="Comma-separated list")
    live_url        = models.URLField(blank=True)
    github_url      = models.URLField(blank=True)
    start_date      = models.DateField(blank=True, null=True)
    end_date        = models.DateField(blank=True, null=True)
    is_published    = models.BooleanField(default=True)
    is_featured     = models.BooleanField(default=False)
    created_at      = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_date']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def tech_list(self):
        return [t.strip() for t in self.tech_stack.split(',') if t.strip()]


# ─────────────────────────────────────────────
# BLOG
# ─────────────────────────────────────────────

class Category(models.Model):
    name        = models.CharField(max_length=100)
    slug        = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Post(models.Model):
    title           = models.CharField(max_length=300)
    slug            = models.SlugField(unique=True, blank=True)
    category        = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    tags            = models.ManyToManyField(Tag, blank=True, related_name='posts')
    author          = models.CharField(max_length=200, default="AutoMex Team")
    author_photo    = models.ImageField(upload_to='authors/', blank=True, null=True)
    excerpt         = models.CharField(max_length=500, blank=True)
    content         = models.TextField()
    cover_image     = models.ImageField(upload_to='blog/', blank=True, null=True)
    is_published    = models.BooleanField(default=True)
    is_featured     = models.BooleanField(default=False)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
