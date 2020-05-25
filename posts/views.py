# -*- coding: utf-8 -*-
#from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import BlogPostForm

# Create your views here.
def get_posts(request):
    """
    Create a view that returns posts that have already been posted
    """
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    
    return render (request, "blogposts.html", {'posts': posts})
    
def post_detail(request, pk):
    """
    Create a view to return a single post object based on the Post ID(pk)
    and render it to postdetail.html template or return a 404 error if no 
    post is found
    """
    post = get_object_or_404(Post, pk=pk)
    post.views += 1
    post.save()
    return render(request, "postdetail.html", {'post': post})
    
def create_or_edit_post(request, pk=None):
    """
    Create a view that allows user to create or edit a post depending 
    if the Post ID is null or not 
    """
    post = get_object_or_404(Post, pk=pk) if pk else None
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect(post_detail, post.pk)
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'blogpostform.html', {'form': form})
    
    