from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from pytils.translit import slugify

from blog.models import BlogPost


class BlogPostListView(ListView):
    """ List"""
    model = BlogPost

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset().order_by(*args, **kwargs)
        queryset = queryset.filter(published=True)
        return queryset


class BlogPostDetailView(DetailView):
    """Detail"""
    model = BlogPost

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views += 1
        self.object.save(update_fields=['views'])
        return self.object


class BlogPostCreateView(CreateView):
    """Create"""
    model = BlogPost
    fields = ('title', 'body', 'image',)
    success_url = reverse_lazy("blog:list")

    def form_valid(self, form):
        if form.is_valid:
            new_object = form.save(commit=False)
            new_object.slug = slugify(new_object.title)
            new_object.save()
            return super().form_valid(form)


class BlogPostUpdateView(UpdateView):
    """Update"""
    model = BlogPost
    fields = ('title', 'body', 'image',)

    def form_valid(self, form):
        if form.is_valid:
            new_object = form.save(commit=False)
            new_object.slug = slugify(new_object.title)
            new_object.save()
            return super().form_valid(form)

    def get_success_url(self):
        return reverse("blog:view", args=[self.kwargs.get("pk")])


class BlogPostDeleteView(DeleteView):
    """Delete"""
    model = BlogPost
    success_url = reverse_lazy("blog:list")


def toggle_publication(request, pk):
    blogpost_item = get_object_or_404(BlogPost, pk=pk)
    if blogpost_item.published:
        blogpost_item.published = False
    else:
        blogpost_item.published = True

    blogpost_item.save()

    return redirect(reverse("blog:list"))
