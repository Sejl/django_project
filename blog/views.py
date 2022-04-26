from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

class PostListView(ListView):
    model = Post
    
    '''django is looking for template in form of
    <app>/<model>_<viewtype>.html
    in our case it is:  blog/post_list.html
    but we're going to use our own home template
    
    for DetailView it is: <app>/<model>_detail.html
    for CreateView it is: <app>/<model>_form.html
    for DeleteView it is: <app>/<model>_confirm_delete.html
    '''
    template_name = 'blog/home.html'
    context_object_name = 'posts' # in listview rename context object name to posts as we already have it in our template
    ordering = ['-date_posted'] # minus sign - from oldest to newest

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


# sticking to conventions in creating detailed post view
class PostDetailView(DetailView):
    model = Post

# we cannot use decorators on clases so we're using mixin

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    # override form valid method
    def form_valid(self, form):
        form.instance.author = self.request.user # before submitting form, set author to current logged user
        return super().form_valid(form)  # running form_valid method from parent but modified


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    # override form valid method
    def form_valid(self, form):
        form.instance.author = self.request.user # before submitting form, set author to current logged user
        return super().form_valid(form)  # running form_valid method from parent but modified        

    def test_func(self): # test if author is the same as the post
        post = self.get_object() 
        if self.request.user == post.author:
            return True
        else:
            return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self): # test if author is the same as the post
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False
