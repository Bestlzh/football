from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render
from django.http import HttpResponse


class BlockIP(MiddlewareMixin):
    def is_block_ip(self,ip):
        return int(ip[-1]) % 2 == 0

    def process_request(self,request):
        ip = request.META['REMOTE_ADDR']
        if self.is_block_ip(ip):

            return HttpResponse('你被屏蔽了')


