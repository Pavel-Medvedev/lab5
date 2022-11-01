from .models import Article
from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User

def archive(request):
    return render(request, 'archive.html', {"posts": Article.objects.all()})

def get_article(request, article_id):
    try:
        post = Article.objects.get(id=article_id)
        return render(request, 'article.html', {"post": post})
    except Article.DoesNotExist:
        raise Http404

def create_post(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = {
                'text': request.POST["text"], 'title': request.POST["title"]
            }
            if form["text"] and form["title"]:
                try:
                    Article.objects.get(title=form["title"])
                    form['errors'] = u"Статья с таким названием уже существует!"
                    return render(request, 'create_post.html', {'form': form});
                except Article.DoesNotExist:
                    article = Article.objects.create(text=form["text"], title=form["title"], author=request.user)
                    return redirect('get_article', article_id=article.id)
            else:
                form['errors'] = u"Не все поля заполнены"
                return render(request, 'create_post.html', {'form': form})
        else:
            return render(request, 'create_post.html', {})
    else:
        raise Http404

def login_user(request):
    if request.method == "POST":
        form = {
            'username': request.POST["username"], 'password': request.POST["password"]
        }
        if form["username"] and form["password"]:
            try:
                User.objects.get(username=form["username"])
                user = authenticate(request, username=form["username"], password=form["password"])
                if user is not None:
                    login(request, user)
                    return redirect('/')
                else:
                    form['errors'] = u"Неверно введён логин или пароль!"
                    return render(request, 'login.html', {'form': form})
            except User.DoesNotExist:
                form['errors'] = u"Ползователя с таким именем нет!"
                return render(request, 'login.html', {'form': form})
        else:
        # если введенные данные некорректны
            form['errors'] = u"Не все поля заполнены"
            return render(request, 'login.html', {'form': form})
    else:
        # просто вернуть страницу с формой, если метод GET
            return render(request, 'login.html', {})


# Create your views here.
