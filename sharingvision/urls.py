# sharingvision/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from articles.views import ArticleListCreate, ArticleDetail  # REST API

urlpatterns = [
    path("admin/", admin.site.urls),

    # === HTML (Django Template) ===
    # Arahkan "/" ke dashboard
    path("", RedirectView.as_view(pattern_name="articles:all_posts", permanent=False)),
    path("", include("articles.urls")),  # /dashboard, /add, /edit/<id>, /trash/<id>, /preview

    # === REST API ===
    path("article/", ArticleListCreate.as_view()),     # GET list (?limit&offset), POST create
    path("article/<int:pk>", ArticleDetail.as_view()), # GET/PUT/PATCH/DELETE by id
]
