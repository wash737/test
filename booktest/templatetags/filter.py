# 自定义过滤器 过滤器本质其实就是python函数

from django.template import Library

#创建Library对象
register = Library()

#自定义的过滤器 最多两个参数 最少一个  |前面为第一个参数 后面传第二个参数   xxx|mode:xxx
@register.filter(name='mode')
def mode(num):
    """判断num是否为偶数"""
    return num % 2 == 0
