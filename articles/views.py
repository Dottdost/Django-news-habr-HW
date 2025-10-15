from django.shortcuts import render, get_object_or_404, redirect
from .models import Article
from .forms import ArticleForm

def home(request):
    articles = Article.objects.all().order_by('-created_at')
    return render(request, 'articles/home.html', {'articles': articles})

def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'articles/detail.html', {'article': article})


def add_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)

            if request.user.is_authenticated:
                article.author = request.user
            else:
                article.author = None

            article.save()
            return redirect('home')
    else:
        form = ArticleForm()

    return render(request, 'articles/add_article.html', {'form': form})
def like_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.likes += 1
    article.save()
    return redirect('article_detail', pk=pk)

def dislike_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.dislikes += 1
    article.save()
    return redirect('article_detail', pk=pk)
