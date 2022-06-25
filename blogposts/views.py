from django.db.models import Count, Q
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from .forms import CommentForm, PostForm
from .models import Post, Category, PostView


def category(request, title):
    category_count = get_category_count()
    category = Category.objects.filter(title=title)[0]
    posts = Post.objects.order_by('-posted')
    categorised_posts = posts.filter(categories=category)
    paginator = Paginator(categorised_posts, 4)
    page_request = 'page'
    n_page = request.GET.get(page_request)
    try:
        paginated_posts = paginator.page(n_page)
    except PageNotAnInteger:
        paginated_posts = paginator.page(1)
    except EmptyPage:
        paginated_posts = paginator.page(paginator.num_pages)
    recent = posts[:3]
    data = {
        'category': category,
        'post_list': paginated_posts,
        'page_request': page_request,
        'recent': recent,
        'categories': category_count
    }
    return render(request, 'category.html', data)


def search(request):
    category_count = get_category_count()
    posts = Post.objects.order_by('-posted')
    query = request.GET.get('q')
    if query:
        posts = posts.filter(Q(title__icontains=query) |
                             Q(overview__icontains=query) |
                             Q(body__icontains=query)).distinct()
    paginator = Paginator(posts, 4)
    page_request = 'page'
    n_page = request.GET.get(page_request)
    try:
        paginated_posts = paginator.page(n_page)
    except PageNotAnInteger:
        paginated_posts = paginator.page(1)
    except EmptyPage:
        paginated_posts = paginator.page(paginator.num_pages)
    data = {
        'post_list': paginated_posts,
        'categories': category_count
    }
    return render(request, 'search_results.html', data)


def get_category_count():
    categories = Post.objects.values('categories__title').annotate(Count('categories__title'))
    return categories


def about(request):
    return render(request, 'about.html', {})


def index(request):
    categories = Category.objects.all()
    featured = Post.objects.filter(featured=True)
    recent = Post.objects.order_by('-posted')[:3]
    data = {
        'featured': featured,
        'recent': recent,
        'categories': categories
    }
    return render(request, 'index.html', data)


def blog(request):
    category_count = get_category_count()
    posts = Post.objects.order_by('-posted')
    paginator = Paginator(posts, 4)
    page_request = 'page'
    n_page = request.GET.get(page_request)
    try:
        paginated_posts = paginator.page(n_page)
    except PageNotAnInteger:
        paginated_posts = paginator.page(1)
    except EmptyPage:
        paginated_posts = paginator.page(paginator.num_pages)
    recent = Post.objects.order_by('-posted')[:3]
    data = {
        'post_list': paginated_posts,
        'page_request': page_request,
        'recent': recent,
        'categories': category_count,
    }
    return render(request, 'blog.html', data)


def post(request, id):
    post = get_object_or_404(Post, id=id)
    category_count = get_category_count()
    recent = Post.objects.order_by('-posted')[:3]
    forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    user_ip = forwarded_for.slit(',')[-1].strip() if forwarded_for else request.META.get('REMOTE_ADDR')
    visited = PostView.objects.filter(user_ip=user_ip, post=post)
    if not visited:
        view = PostView()
        view.user_ip = user_ip
        view.post = post
        view.save()
    form = CommentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.post = post
            form.save()
            return redirect('post_details', id=post.id)

    data = {
        'post': post,
        'recent': recent,
        'categories': category_count,
        'form': form
    }
    return render(request, 'post.html', data)


def create(request):
    title = 'Create'
    form = PostForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('post_details', id=form.instance.id)
    data = {
        'title': title,
        'form': form
    }
    return render(request, 'create.html', data)


def post_edit(request, id):
    title = 'Edit'
    post = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('post_details', id=form.instance.id)
    data = {
        'title': title,
        'form': form
    }
    return render(request, 'create.html', data)


def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect('blog_posts')