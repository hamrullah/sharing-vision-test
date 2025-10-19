# articles/urls.py
from django.urls import path
from . import views_html as views

app_name = "articles"

urlpatterns = [
    path("dashboard/", views.all_posts, name="all_posts"),
    path("add/", views.add_new, name="add_new"),
    path("edit/<int:pk>/", views.edit_post, name="edit"),
    path("trash/<int:pk>/", views.move_to_trash, name="trash"),
    path("preview/", views.preview, name="preview"),
]
