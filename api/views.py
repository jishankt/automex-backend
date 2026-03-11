"""
AutoMex – Consolidated API Views
All endpoints live in one file, one app.
"""

from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    CompanyInfo, TeamMember, ContactSubmission,
    Client, Testimonial,
    Service,
    Project,
    Category, Tag, Post,
)
from .serializers import (
    CompanyInfoSerializer, TeamMemberSerializer, ContactSubmissionSerializer,
    ClientSerializer, TestimonialSerializer,
    ServiceSerializer,
    ProjectSerializer,
    CategorySerializer, TagSerializer, PostListSerializer, PostDetailSerializer,
)


# ═══════════════════════════════════════════════
# COMPANY / HOME DATA
# ═══════════════════════════════════════════════

class CompanyInfoView(APIView):
    """GET /api/company/  → full company info + team"""

    def get(self, request):
        company = CompanyInfo.objects.first()
        if not company:
            return Response({'detail': 'Company info not set up yet.'}, status=404)
        serializer = CompanyInfoSerializer(company, context={'request': request})
        return Response(serializer.data)


class HomeView(APIView):
    """
    GET /api/home/
    Returns everything the home page needs in one shot:
      - company info
      - featured services (up to 3)
      - featured projects (up to 3)
      - active clients
      - featured testimonials
      - team members (up to 4)
    """

    def get(self, request):
        company      = CompanyInfo.objects.first()
        team         = TeamMember.objects.filter(is_active=True)[:4]
        clients      = Client.objects.filter(is_active=True).order_by('order')
        testimonials = Testimonial.objects.filter(is_approved=True, is_featured=True)
        services     = Service.objects.filter(is_active=True, is_featured=True).order_by('order')[:3]
        projects     = Project.objects.filter(is_published=True, is_featured=True)[:3]

        data = {
            'company':      CompanyInfoSerializer(company, context={'request': request}).data if company else None,
            'team':         TeamMemberSerializer(team, many=True, context={'request': request}).data,
            'clients':      ClientSerializer(clients, many=True, context={'request': request}).data,
            'testimonials': TestimonialSerializer(testimonials, many=True, context={'request': request}).data,
            'services':     ServiceSerializer(services, many=True, context={'request': request}).data,
            'projects':     ProjectSerializer(projects, many=True, context={'request': request}).data,
        }
        return Response(data)


# ═══════════════════════════════════════════════
# ABOUT
# ═══════════════════════════════════════════════

class AboutView(APIView):
    """GET /api/about/  → company info + full team"""

    def get(self, request):
        company = CompanyInfo.objects.first()
        team    = TeamMember.objects.filter(is_active=True)
        data = {
            'company': CompanyInfoSerializer(company, context={'request': request}).data if company else None,
            'team':    TeamMemberSerializer(team, many=True, context={'request': request}).data,
        }
        return Response(data)


# ═══════════════════════════════════════════════
# CONTACT
# ═══════════════════════════════════════════════

class ContactView(APIView):
    """
    POST /api/contact/
    Accepts: name, email, phone, company, subject, message
    Saves submission and sends e-mail notifications.
    """

    def post(self, request):
        serializer = ContactSubmissionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        submission = serializer.save()
        company    = CompanyInfo.objects.first()
        admin_email   = company.email if company else 'automextechnologies@gmail.com'
        company_name  = company.name  if company else 'AutoMex'

        # ── Admin notification ──────────────────────
        try:
            send_mail(
                subject=f'New Contact Form Submission: {submission.subject}',
                message=(
                    f'Name: {submission.name}\n'
                    f'Email: {submission.email}\n'
                    f'Phone: {submission.phone}\n'
                    f'Company: {submission.company}\n\n'
                    f'Message:\n{submission.message}\n\n'
                    f'Submitted at: {submission.submitted_at}'
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[admin_email],
                fail_silently=True,
            )
        except Exception as e:
            print(f'Admin email error: {e}')

        # ── Thank-you to client ─────────────────────
        try:
            send_mail(
                subject=f'Thank You for Contacting {company_name}',
                message=(
                    f'Dear {submission.name},\n\n'
                    f'Thank you for reaching out to {company_name}! '
                    f'We have received your message and will get back to you within 24 hours.\n\n'
                    f'Subject: {submission.subject}\n\n'
                    f'Best regards,\n{company_name} Team\n{admin_email}\nCalicut, Palayam\n\n'
                    f'---\nThis is an automated response. Please do not reply to this email.'
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[submission.email],
                fail_silently=True,
            )
        except Exception as e:
            print(f'Client email error: {e}')

        return Response(
            {'message': 'Thank you! We have received your message and sent a confirmation to your inbox.'},
            status=status.HTTP_201_CREATED,
        )


# ═══════════════════════════════════════════════
# CLIENTS & TESTIMONIALS
# ═══════════════════════════════════════════════

class ClientListView(generics.ListAPIView):
    """GET /api/clients/"""
    serializer_class = ClientSerializer

    def get_queryset(self):
        return Client.objects.filter(is_active=True).order_by('order')


class TestimonialListView(generics.ListAPIView):
    """GET /api/testimonials/   ?featured=true"""
    serializer_class = TestimonialSerializer

    def get_queryset(self):
        qs = Testimonial.objects.filter(is_approved=True)
        if self.request.query_params.get('featured'):
            qs = qs.filter(is_featured=True)
        return qs


# ═══════════════════════════════════════════════
# SERVICES
# ═══════════════════════════════════════════════

class ServiceListView(generics.ListAPIView):
    """GET /api/services/"""
    serializer_class = ServiceSerializer

    def get_queryset(self):
        return Service.objects.filter(is_active=True).order_by('order')


class ServiceDetailView(generics.RetrieveAPIView):
    """GET /api/services/<slug>/"""
    serializer_class   = ServiceSerializer
    lookup_field       = 'slug'

    def get_queryset(self):
        return Service.objects.filter(is_active=True)


# ═══════════════════════════════════════════════
# PROJECTS
# ═══════════════════════════════════════════════

class ProjectListView(generics.ListAPIView):
    """
    GET /api/projects/
    Query params: ?category=web  ?featured=true
    """
    serializer_class = ProjectSerializer

    def get_queryset(self):
        qs = Project.objects.filter(is_published=True)
        category = self.request.query_params.get('category')
        if category:
            qs = qs.filter(category=category)
        if self.request.query_params.get('featured'):
            qs = qs.filter(is_featured=True)
        return qs


class ProjectDetailView(generics.RetrieveAPIView):
    """GET /api/projects/<slug>/"""
    serializer_class = ProjectSerializer
    lookup_field     = 'slug'

    def get_queryset(self):
        return Project.objects.filter(is_published=True)


class ProjectCategoriesView(APIView):
    """GET /api/projects/categories/  → list of valid category choices"""

    def get(self, request):
        categories = [{'value': k, 'label': v} for k, v in Project.PROJECT_CATEGORIES]
        return Response(categories)


# ═══════════════════════════════════════════════
# BLOG
# ═══════════════════════════════════════════════

class PostListView(generics.ListAPIView):
    """
    GET /api/blog/
    Query params: ?q=search  ?category=slug  ?tag=slug  ?featured=true
    """
    serializer_class = PostListSerializer

    def get_queryset(self):
        qs = Post.objects.filter(is_published=True)

        query = self.request.query_params.get('q')
        if query:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(excerpt__icontains=query) |
                Q(content__icontains=query) |
                Q(tags__name__icontains=query)
            ).distinct()

        category_slug = self.request.query_params.get('category')
        if category_slug:
            qs = qs.filter(category__slug=category_slug)

        tag_slug = self.request.query_params.get('tag')
        if tag_slug:
            qs = qs.filter(tags__slug=tag_slug)

        if self.request.query_params.get('featured'):
            qs = qs.filter(is_featured=True)

        return qs


class PostDetailView(generics.RetrieveAPIView):
    """GET /api/blog/<slug>/"""
    serializer_class = PostDetailSerializer
    lookup_field     = 'slug'

    def get_queryset(self):
        return Post.objects.filter(is_published=True)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        related  = Post.objects.filter(
            is_published=True, category=instance.category
        ).exclude(id=instance.id)[:3]

        return Response({
            'post':          PostDetailSerializer(instance, context={'request': request}).data,
            'related_posts': PostListSerializer(related, many=True, context={'request': request}).data,
        })


class BlogCategoryListView(generics.ListAPIView):
    """GET /api/blog/categories/"""
    serializer_class = CategorySerializer
    queryset         = Category.objects.all()


class TagListView(generics.ListAPIView):
    """GET /api/blog/tags/"""
    serializer_class = TagSerializer
    queryset         = Tag.objects.all()
