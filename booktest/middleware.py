"""中间件 """
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class Middleware(MiddlewareMixin):

    EXCLUDE_IPS = ["127.0.0.1"]

    def process_view(self, request, view_func, view_args, view_kwargs):
        """试图函数调用之前会调用 这个函数的名字是固定的 是python预留的  必须定义在类中  然后将类注册到setting中"""
        user_ip = request.META["REMOTE_ADDR"]
        if user_ip in Middleware.EXCLUDE_IPS:
            return HttpResponse("<h1>禁止访问</h1>")


class MiddlewareTest(MiddlewareMixin):

    def __init__(self, get_response):
        """服务重启之后接收第一个请求时调用 只调用一次"""
        print("----------------__init__-----------------")
        self.get_response = get_response

    def process_request(self, request):
        """产生request之后，url匹配之前调用"""
        print("----------------process_request-----------------")

    def process_view(self, request, view_func, *view_args, ** view_kwargs):
        """匹配url之后，视图函数调用之前调用"""
        print("----------------process_view-----------------")

    def process_response(self, request, response):
        """视图函数调用之后, nr返回给浏览器之前调用"""
        print("----------------process_response-----------------")
        return response


class ExceptionMiddlewareTest(MiddlewareMixin):
    def process_exception(self, request, exception):
        """视图函数发生异常时调用"""
        print("----------------process_exception-----------------")