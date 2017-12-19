import logging

logger = logging.getLogger('inf')
#
def statistic(view_func):
    def wrap(request,*args,**kwargs):
        ip = request.META['REMOTE_ADDR']
        aid = args[0]
        logger.info('logging'+" : " + str(aid)+" , "+str(ip))
        return view_func(request,*args,**kwargs)
    return wrap
