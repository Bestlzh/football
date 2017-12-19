import logging

logger = logging.getLogger('inf')



#装饰器实现打印访问的文章id和访问者的ip
def statistic(view_func):
    def wrap(request,*args,**kwargs):
        ip = request.META['REMOTE_ADDR']
        aid = args[0]
        logger.info('logging'+" : " + str(aid)+" , "+str(ip))
        return view_func(request,*args,**kwargs)
    return wrap
