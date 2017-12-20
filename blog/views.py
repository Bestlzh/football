import random
import math
import redis
import logging
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.core.cache import cache
from blog.models import Article,BlogComment
from blog.forms import PublishForm
from .helper import statistic,page_cache,page_cache_two,read_counter

# 页面缓存装饰器
from django.views.decorators.cache import cache_page
# Create your views here.

r = redis.Redis()
# blog 首页
def index(request):
    # 分页
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


    # 分页的另一种
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
@statistic   #日志打印
@read_counter   #统计点击次数
# @page_cache   #自己的页面缓存
# @page_cache_two(100)   #自己页面缓存
# @cache_page(60)  #页面缓存装饰器  参数为过期时间  单位秒
def content(request,*args, **kwargs):

    # 不使用装饰器的页面缓存
    article = cache.get('article'+str(args[0]))
    if article is None:
        article = Article.objects.filter(id=args[0]).first()
        cache.set('article'+str(args[0]),article,)

    # article = Article.objects.filter(id=args[0]).first()
    # redis统计点击次数，不使用装饰器
    # key = 'sort_article'
    # r.zincrby(key,str(args[0]))  #自加一


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


# 文章标题搜索
def search(request):
    q = request.GET.get('sreach')
    if not q:
        return HttpResponseRedirect(reverse('blog:index'))

    articles = Article.objects.filter(title__icontains=q)
    context = {'articles':articles}
    return render(request, 'blog/index.html', context)


# 编辑，发表
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


# 文章点击量排序
def sort_article(request):
    key = 'sort_article'
    r.zrevrange(key,0,10)
        #去除前十的文章id，和访次数
    a_list = [(int(aid),int(count)) for aid,count in r.zrevrange(key, 0, 10, withscores=True)]
    # 文章id  按访问量排序的
    aid_list = [aid[0] for aid in a_list]
    print(aid_list)
    # 取出文章对象的 队列  不是按照访问量进行排序的
    articles_list = Article.objects.filter(id__in=aid_list)
    # 将文章id与文章对象，写入字典，不是按照访问量进行排序的
    articles_dict = {article.id: article for article in articles_list}
    # 按照排好序的id  取出文章对象
    articles = [articles_dict[aid] for aid in aid_list]
    context = {'articles': articles}
    return render(request, 'blog/index.html', context)


    '''测试'''
    # 取出文章对象  跟访问量
    # article_count = [(articles_dict[aid],count) for aid,count in a_list]
    # return render(request, 'blog/sort.html', {'article_count':article_count})


