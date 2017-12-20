import logging
import redis
from django.core.cache import cache
logger = logging.getLogger('inf')
from blog.models import Article


r = redis.Redis()


#装饰器实现打印访问的文章id和访问者的ip
def statistic(view_func):
    def wrap(request,*args,**kwargs):
        ip = request.META['REMOTE_ADDR']
        aid = args[0]
        logger.info('logging'+" : " + str(aid)+" , "+str(ip))
        return view_func(request,*args,**kwargs)
    return wrap


# 页面缓存
def page_cache(view_func):
    def wrap(request,*args,**kwargs):
        key = 'page-'+request.get_full_path()
        response = cache.get(key)
        if response in None:
            response = view_func(request,*args,**kwargs)
            cache.set('key',response)
        return view_func(request,*args,**kwargs)
    return wrap


# 带过期时间的缓存装饰器
def page_cache_two(timeout):
    def wrap1(view_func):
        def wrap2(request,*args,**kwargs):
            key = "page-%s"%(request.get_full_path())
            response = cache.get(key)
            if response is None:
                response = view_func(request,*args,**kwargs)
                cache.set(key,response,timeout)
        return wrap2

    return wrap1



#点击次数装饰器

def read_counter(view_func):
    def wrap(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)

        if response.status_code == 200:
            key = 'read_counter'
            r.zincrby(key, str(args[0]))  # 自加一
        return response
    return wrap


# 文章点击排序前十,可在index的views调用，将其返回到index页面
def sort_article():
    key = 'sort_article'
    r.zrevrange(key, 0, 10)
    a_list = [(int(aid), int(count)) for aid, count in r.zrevrange(key, 0, 10, withscores=True)]
    aid_list = [aid[0] for aid in a_list]
    print(aid_list)
    articles = Article.objects.filter(id__in=aid_list)
    articles_dict = {article.id: article for article in articles}
    return [ (articles_dict[aid], count) for aid, count in a_list]
