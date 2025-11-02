from django.contrib.auth import get_user_model
User = get_user_model()
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Article, Bookmark, Vote
from .forms import ArticleForm
from .models import CATEGORIES


def home(request):
    articles = Article.objects.filter(status='PUBLISHED').order_by('-created_at')
    return render(request, 'articles/home.html', {'articles': articles})



def category_articles(request, category):
    articles = Article.objects.filter(category=category, status='PUBLISHED')
    return render(request, 'articles/category.html', {'articles': articles, 'category': category})
def categories_list(request):
    return render(request, 'articles/categories.html', {'categories': CATEGORIES})
def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)

    user_vote = None
    if request.user.is_authenticated:
        user_vote = Vote.objects.filter(article=article, user=request.user).first()

    is_bookmarked = False
    if request.user.is_authenticated:
        is_bookmarked = Bookmark.objects.filter(article=article, user=request.user).exists()

    context = {
        'article': article,
        'user_vote': user_vote,
        'is_bookmarked': is_bookmarked
    }
    return render(request, 'articles/detail.html', context)


@login_required
def add_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.status = 'PENDING'
            article.save()
            return redirect('home')
    else:
        form = ArticleForm()

    return render(request, 'articles/add_article.html', {'form': form})


@login_required
def edit_article(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if article.author != request.user:
        messages.error(request, "You cannot edit other people's articles.")
        return redirect('article_detail', pk=pk)

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            article.status = 'PENDING'
            article.save()
            messages.info(request, "The changes have been sent to the administrator for review.")
            return redirect('article_detail', pk=pk)
    else:
        form = ArticleForm(instance=article)

    return render(request, 'articles/edit_article.html', {'form': form, 'article': article})


@login_required
def vote_article(request, pk, value):
    value = int(value)
    article = get_object_or_404(Article, pk=pk)
    vote, created = Vote.objects.get_or_create(article=article, user=request.user, defaults={'value': value})

    if not created:
        if vote.value != value:
            vote.value = value
            vote.save()
        else:
            vote.delete()
            if value == 1:
                article.likes = max(0, article.likes - 1)
            else:
                article.dislikes = max(0, article.dislikes - 1)
            article.calculate_rating()
            article.save(update_fields=['likes', 'dislikes', 'avg_rating'])
            return redirect('article_detail', pk=pk)

    article.likes = Vote.objects.filter(article=article, value=1).count()
    article.dislikes = Vote.objects.filter(article=article, value=-1).count()
    article.calculate_rating()
    article.save(update_fields=['likes', 'dislikes', 'avg_rating'])

    return redirect('article_detail', pk=pk)


@login_required
def toggle_bookmark(request, pk):
    article = get_object_or_404(Article, pk=pk)
    bookmark, created = Bookmark.objects.get_or_create(article=article, user=request.user)
    if not created:
        bookmark.delete()
    return redirect('article_detail', pk=pk)


def popular_articles(request):
    articles = Article.objects.filter(status='PUBLISHED', avg_rating__gte=4).order_by('-avg_rating')
    return render(request, 'articles/popular.html', {'articles': articles})


def category_articles(request, category):
    articles = Article.objects.filter(category=category, status='PUBLISHED').order_by('-created_at')
    return render(request, 'articles/category.html', {'articles': articles, 'category': category})


@login_required
def favorite_articles(request):
    bookmarks = Bookmark.objects.filter(user=request.user).select_related('article')
    articles = [b.article for b in bookmarks]
    return render(request, 'articles/favorites.html', {'articles': articles})


def is_admin(user):
    return user.is_staff or user.is_superuser


@user_passes_test(is_admin)
def approve_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.status = 'PUBLISHED'
    article.save()
    messages.success(request, f"Article «{article.title}» published!")
    return redirect('home')


@user_passes_test(is_admin)
def pending_articles(request):
    articles = Article.objects.filter(status='PENDING').order_by('-created_at')
    return render(request, 'articles/pending.html', {'articles': articles})


@user_passes_test(is_admin)
def reject_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.status = 'DRAFT'
    article.save()
    messages.warning(request, f"Article «{article.title}» returned to drafts.")
    return redirect('home')


def admin_required(view):
    return user_passes_test(lambda u: u.is_staff)(view)


@admin_required
def users_list(request):
    users = User.objects.all()
    return render(request, 'articles/users_list.html', {'users': users})


@admin_required
def toggle_staff(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.is_staff = not user.is_staff
    user.save()
    return redirect('users_list')


@admin_required
def toggle_active(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.is_active = not user.is_active
    user.save()
    return redirect('users_list')
