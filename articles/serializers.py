# articles/serializers.py
from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id","title","content","category","created_date","updated_date","status"]

    def validate_title(self, v):
        if len(v) < 20:
            raise serializers.ValidationError("Title minimal 20 karakter.")
        return v

    def validate_content(self, v):
        if len(v) < 200:
            raise serializers.ValidationError("Content minimal 200 karakter.")
        return v

    def validate_category(self, v):
        if len(v) < 3:
            raise serializers.ValidationError("Category minimal 3 karakter.")
        return v

    def validate_status(self, v):
        allowed = {c.value for c in Post.Status}
        if v not in allowed:
            raise serializers.ValidationError("Status harus salah satu dari: publish | draft | trash")
        return v
