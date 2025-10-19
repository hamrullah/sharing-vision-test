# articles/views_html.py
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib import messages

from .models import Post
from .forms import PostForm

PAGE_SIZE_DEFAULT = 10

def all_posts(request):
    """
    /dashboard/?tab=publish&limit=10&offset=0
    """
    tab = request.GET.get("tab", "publish")  # publish|draft|trash
    limit = int(request.GET.get("limit", PAGE_SIZE_DEFAULT))
    offset = int(request.GET.get("offset", 0))
    if limit < 1: limit = 1
    if limit > 100: limit = 100
    if offset < 0: offset = 0

    qs = Post.objects.all()
    if tab in {"publish", "draft", "trash"}:
        qs = qs.filter(status=tab)

    # manual limit/offset agar sesuai permintaan
    total = qs.count()
    rows = qs[offset: offset + limit]

    context = {
        "tab": tab,
        "rows": rows,
        "count": total,
        "limit": limit,
        "offset": offset,
        "next_offset": offset + limit,
        "prev_offset": max(0, offset - limit),
    }
    return render(request, "articles/all_posts.html", context)


def add_new(request):
    """
    /add — tombol Publish & Draft
    """
    initial_status = request.GET.get("status") or "draft"
    if request.method == "POST":
        form = PostForm(request.POST)
        # tombol menentukan status
        action_status = request.POST.get("action_status")  # "publish" | "draft"
        if action_status:
            form.data = form.data.copy()
            form.data["status"] = action_status
        if form.is_valid():
            form.save()
            messages.success(request, "Artikel berhasil disimpan.")
            return redirect(reverse("articles:all_posts"))
    else:
        form = PostForm(initial={"status": initial_status})
    return render(request, "articles/add_edit.html", {"form": form, "mode": "add"})


def edit_post(request, pk):
    """
    /edit/<id> — tombol Publish & Draft
    """
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        action_status = request.POST.get("action_status")
        if action_status:
            form.data = form.data.copy()
            form.data["status"] = action_status
        if form.is_valid():
            form.save()
            messages.success(request, "Artikel diperbarui.")
            return redirect(reverse("articles:all_posts"))
    else:
        form = PostForm(instance=post)
    return render(request, "articles/add_edit.html", {"form": form, "mode": "edit", "post": post})


def move_to_trash(request, pk):
    """
    POST /trash/<id> — konfirmasi via modal
    """
    post = get_object_or_404(Post, pk=pk)
    post.status = "trash"
    post.save(update_fields=["status"])
    messages.info(request, "Artikel dipindahkan ke Trash.")
    return redirect(request.META.get("HTTP_REFERER") or reverse("articles:all_posts"))


def preview(request):
    """
    /preview — daftar kartu untuk status publish + pagination
    """
    limit = int(request.GET.get("limit", PAGE_SIZE_DEFAULT))
    page = int(request.GET.get("page", 1))
    if limit < 1: limit = 1
    if limit > 100: limit = 100

    qs = Post.objects.filter(status="publish").order_by("-created_date")
    paginator = Paginator(qs, limit)
    try:
        page_obj = paginator.page(page)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(request, "articles/preview.html", {"page_obj": page_obj, "limit": limit})
