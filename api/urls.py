"""
AutoMex API – URL Configuration
Mount this in your project urls.py as:
    path('api/', include('api.urls')),
"""

from django.urls import path
from . import views

urlpatterns = [

    # ── Company / Pages ────────────────────────
    path('home/',    views.HomeView.as_view(),        name='home'),
    path('about/',   views.AboutView.as_view(),       name='about'),
    path('company/', views.CompanyInfoView.as_view(), name='company-info'),
    path('contact/', views.ContactView.as_view(),     name='contact'),

    # ── Clients & Testimonials ──────────────────
    path('clients/',      views.ClientListView.as_view(),      name='client-list'),
    path('testimonials/', views.TestimonialListView.as_view(), name='testimonial-list'),

    # ── Services ───────────────────────────────
    path('services/',        views.ServiceListView.as_view(),   name='service-list'),
    path('services/<slug:slug>/', views.ServiceDetailView.as_view(), name='service-detail'),

    # ── Projects ───────────────────────────────
    path('projects/',                  views.ProjectListView.as_view(),       name='project-list'),
    path('projects/categories/',       views.ProjectCategoriesView.as_view(), name='project-categories'),
    path('projects/<slug:slug>/',      views.ProjectDetailView.as_view(),     name='project-detail'),

    # ── Blog ───────────────────────────────────
    path('blog/',                  views.PostListView.as_view(),        name='post-list'),
    path('blog/categories/',       views.BlogCategoryListView.as_view(),name='blog-categories'),
    path('blog/tags/',             views.TagListView.as_view(),         name='tag-list'),
    path('blog/<slug:slug>/',      views.PostDetailView.as_view(),      name='post-detail'),
]
