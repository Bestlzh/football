import random
import math
import logging
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect

from blog.models import Article,BlogComment
from blog.forms import PublishForm
from .helper import statistic


# 页面缓存装饰器
from django.views.decorators.cache import cache_page
# Create your views here.


# blog 首页
# @cache_page(600)  #页面缓存装饰器  参数为过期时间  单位秒
def index(request):

    articles_list = Article.objects.all()
    paginator = Paginator(articles_list, 5)
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        articles = paginator.page(1)
    pages_range=range(1,articles.paginator.num_pages+1)



    # pages = math.ceil(Article.objects.count() / 5)  # 页码数
    # page = int(request.GET.get('page', 1))
    # page = (page - 1) if 1 <= page <= pages else 0
    # start = page * 5
    # end = (page + 1) * 5
    # articles = Article.objects.all()[start:end]
    # pages_range=range(1,pages+1)
    context = {'articles':articles,'pages_range':pages_range}
    return render(request, 'blog/index.html', context)


# 文章详情页
@statistic
def content(request,*args, **kwargs):
    article = Article.objects.filter(id=args[0]).first()
    if request.method == 'POST':
        num = random.randint(1,99999)
        username = '游客'+str(num)
        comment = request.POST.get('comment')
        # 判断是否输入空
        if comment != '':
            # 判断是否有父评论
            if len(args) > 1:
                parent = BlogComment.objects.filter(id = args[1]).first()
            else:
                parent = None
            com = BlogComment.comment_text(username, article, comment, parent)
            com.save()
    comments = BlogComment.objects.filter(article=article)
    context = {'article':article,'comments':comments}
    return render(request,'blog/content.html',context)


# 发表文章
# def publish(request):
#     # form = PublishForm()
#     # return render(request,'blog/publish.html')
#     if request.method == "POST":
#         author='作者'
#         title = request.POST.get("title")
#         content = request.POST.get("content")
#         art = Article.publish_article(author,title,content)
#         art.save()
#         return HttpResponseRedirect(reverse('blog:index'))
#     else:
#         context = {}
#         return render(request,'blog/publish.html',context)


# 文章标题搜索
def search(request):
    q = request.GET.get('sreach')
    if not q:
        return HttpResponseRedirect(reverse('blog:index'))

    articles = Article.objects.filter(title__icontains=q)
    context = {'articles':articles}
    return render(request, 'blog/index.html', context)


# 编辑
def publish(request,*args):
    if request.method == 'POST':
        # print('____________________________________________________')
        form = PublishForm(request.POST)
        if form.is_valid():
            aid = form.cleaned_data['aid']
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']

            article = Article.objects.get(id=aid)
            article.title = title
            article.content = content

            article.save()

            return HttpResponseRedirect(reverse('blog:index'))
        # 发表文章的提交
        else:
            author = '作者'+str(random.randint(1,99999))
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']

            art = Article.publish_article(author,title,content)
            art.save()
            return HttpResponseRedirect(reverse('blog:index'))
    else:
        if len(args) == 0:
            context = {}
            return render(request, 'blog/publish.html', context)
        article = Article.objects.get(id=args[0])
        context = {'article':article}
        return render(request, 'blog/publish.html', context)
