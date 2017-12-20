from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse


# 中间件实现ip拦截
class BlockIP(MiddlewareMixin):
    def is_block_ip(self,ip):
        return int(ip[-1]) % 2 == 0

    def process_request(self,request):
        ip = request.META['REMOTE_ADDR']
        if self.is_block_ip(ip):
            return HttpResponse('你被屏蔽了')


