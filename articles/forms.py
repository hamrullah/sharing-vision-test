# articles/forms.py
from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "category", "status"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "border rounded-xl px-3 py-2 w-full",
                "minlength": "20",
                "placeholder": "Minimal 20 karakter",
                "required": True,
            }),
            "content": forms.Textarea(attrs={
                "class": "border rounded-xl px-3 py-2 w-full",
                "rows": 8,
                "minlength": "200",
                "placeholder": "Minimal 200 karakter",
                "required": True,
            }),
            "category": forms.TextInput(attrs={
                "class": "border rounded-xl px-3 py-2 w-full",
                "minlength": "3",
                "placeholder": "Minimal 3 karakter",
                "required": True,
            }),
            "status": forms.Select(attrs={
                "class": "border rounded-xl px-3 py-2 w-full",
                "required": True,
            }),
        }

    # server-side validation (sama seperti serializer)
    def clean_title(self):
        v = self.cleaned_data["title"]
        if len(v) < 20:
            raise forms.ValidationError("Title minimal 20 karakter.")
        return v

    def clean_content(self):
        v = self.cleaned_data["content"]
        if len(v) < 200:
            raise forms.ValidationError("Content minimal 200 karakter.")
        return v

    def clean_category(self):
        v = self.cleaned_data["category"]
        if len(v) < 3:
            raise forms.ValidationError("Category minimal 3 karakter.")
        return v
