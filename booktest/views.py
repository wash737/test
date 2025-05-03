from io import BytesIO

from django.core.files.uploadedfile import TemporaryUploadedFile
from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader, RequestContext
from .models import HeroInfo, BookInfo, Pictest, AreaInfo
from PIL import Image, ImageDraw, ImageFont
import random
import string
from django.core.paginator import Paginator
from django.conf import settings  # 访问配置文件的
import json


# 登录装饰器
def login_required(func):
    def call_func(request, *args, **kwargs):
        if not request.session.has_key("islogin"):
            return redirect("/login")
        else:
            return func(request, *args, **kwargs)
    return call_func

EXCLUDE_IPS = ["127.0.0.1"]
#禁止ip访问
def blocked_id(func):
    def call_func(request, *args, **kwargs):
        user_ip = request.META["REMOTE_ADDR"]
        if user_ip in EXCLUDE_IPS:
            return HttpResponse("<h1>禁止访问</h1>")
        else:
            return func(request, *args, **kwargs)
    return call_func


def index(request):
    print("---------index-----------")
    return render(request, "booktest/index.html")


def temp_tags(request):
    books = BookInfo.objects.all()
    return render(request, "booktest/temp_tags.html", {"books": books})


def temp_filter(request):
    books = BookInfo.objects.all()
    return render(request, "booktest/temp_filter.html", {"books": books})


def temp_inhreit(request):
    """模板继承"""
    return render(request, "booktest/child.html")


def html_escape(request):
    """html转义"""
    return render(request, "booktest/html_escape.html", {"content": "<h1>hello</h1>"})
    #return render(request, "booktest/html_escape.html", {"content": "&lth1&gthello&lt/h1&gt"})


def login(request):
    # 判断用户是否登录
    if request.session.has_key("islogin"):
        # 用户已经登录 跳转到修改密码
        return redirect("/check_pwd")
    else:
        if "usermame" in request.COOKIES:
            usermame = request.COOKIES["usermame"]
        else:
            usermame = ""
        return render(request, "booktest/login.html", {"usermame": usermame})


def login_check(request):
    """校验登录"""
    post = request.POST
    username = post.get("username")
    password = post.get("password")
    remeber = post.get("remeber")
    vcode = post.get("vcode")
    session_vcode = request.session.get("vcode")
    if vcode != session_vcode:
        return render(request, "booktest/login.html", {"errmessage": "验证码错误"})
    if username == "111" and password == "111":
        response = redirect("/check_pwd")
        if remeber == "on":
            response.set_cookie("usermame", username, max_age=7*24*60*60)
        #记住用户的登录状态 设置session
        request.session["islogin"] = True
        request.session["username"] = username
        return response
    else:
        return render(request, "booktest/login.html", {"errmessage":"用户名或密码错误"})


@login_required
def check_pwd(request):
    return render(request, "booktest/check_pwd.html")


@login_required
def check_pwd_action(request):
    pwd = request.POST.get("password_new")
    username = request.session.get("username")
    return HttpResponse("%s修改成功密码为%s" % (username, pwd))


def generate_captcha(request):
    # 生成随机字符串（字母+数字）
    characters = string.ascii_letters + string.digits
    captcha_text = ''.join(random.choice(characters) for _ in range(4))

    # 创建图片对象
    width = 100
    height = 25
    bgcolor = (random.randrange(20, 100), random.randrange(20, 100), 255)
    image = Image.new('RGB', (width, height), bgcolor)
    draw = ImageDraw.Draw(image)

    # 加载字体（使用系统默认字体或指定字体文件）
    try:
        font = ImageFont.truetype("arial.ttf", 22)
    except:
        font = ImageFont.load_default()

    x = 5
    for char in captcha_text:
        # 随机颜色和位置偏移
        color = (255, 255, 255)
        y_offset = random.randint(-5, 5)
        draw.text((x, 2 + y_offset), char, fill=color, font=font)
        x += 20 + random.randint(-5, 5)  # 字符间距随机变化

    # 添加干扰线
    # for _ in range(5):
    #     start = (random.randint(0, width), random.randint(0, height))
    #     end = (random.randint(0, width), random.randint(0, height))
    #     draw.line([start, end], fill=(random.randint(0, 200), random.randint(0, 200), random.randint(0, 200)), width=2)

    # 添加噪点
    for _ in range(500):
        xy = (random.randint(0, width), random.randint(0, height))
        draw.point(xy, fill=(random.randint(0, 255), 255, random.randint(0, 255)))

    # 扭曲变形（简单实现）
    # image = image.transform(
    #     (width, height),
    #     Image.AFFINE,
    #     (1, random.uniform(-0.2, 0.2), 0,
    #      random.uniform(-0.2, 0.2), 1, 0)
    # )
    request.session["verifycode"] = captcha_text
    buf = BytesIO()
    image.save(buf, 'png')
    return HttpResponse(buf.getvalue(), "image/png")


def url_reverse(request):
    return render(request, "booktest/url_reverse.html")


def static_test(request):
    basedir = settings.BASE_DIR
    staticdir = settings.STATICFILES_DIRS
    staticfinders = settings.STATICFILES_FINDERS
    return render(request, "booktest/static_test.html", {"basedir":basedir, "staticdir":staticfinders})

#@blocked_id
def index1(request):
    """获取浏览器断的ip"""
    ip = request.META["REMOTE_ADDR"]
    print(ip)
    # 禁止某些ip访问  可以使用中间件 也可以使用装饰器  这里装饰器注释掉 使用中间件  中间件在middleware.py这个文件中
    return render(request, "booktest/index.html")


def show_upload(request):
    """上传图片"""
    return render(request, "booktest/upload_pic.html")


def upload_handle(request):
    """上传图片处理"""
    # 获取上传的图片 返回文件的处理对象
    pic = request.FILES.get("pic")
    #pic.chunks()  # 获取文件的生成器  每次返回一部分内容 可以遍历他获取文件的所有内容
    print(type(pic))
    print(pic.name) # 获取文件名称
    """
    返回的类型为TemporaryUploadedFile 或者 MemoryUploadedFile  
    是根据文件大小返回不同的对象 
    <=2.5M 放到内存中   返回MemoryUploadedFile
    >2.5M 放到一个临时文件中 返回TemporaryUploadedFile
    django.core.files.uploadedfile.TemporaryUploadedFile
    django.core.files.uploadedfile.MemoryUploadedFile
    """
    # 创建一个文件
    save_path = "%s/booktest/%s" %(settings.MEDIA_ROOT, pic.name)
    # 获取上传文件的内容 并写到创建的文件中
    with open(save_path, "wb") as f:
        for content in pic.chunks():
            f.write(content)
    # 保存地址到数据库
    Pictest.objects.create(gpic="booktest/%s" % pic.name)
    return HttpResponse("上传成功")


def show_area(request, num):
    """分页"""
    # 查询所有省级地区信息
    areas = AreaInfo.objects.filter(aParent=0)
    # 分页 每页显示10条
    pt = Paginator(areas, 10)
    countpage = pt.num_pages # 返回分页之后的总页数
    pageList = pt.page_range # 返回分页之后的页码的列表
    # 获取页的内容
    if num:
        page = pt.page(int(num))
    else:
        page = pt.page(1)
    currentpage = page.number   # 返回当前页
    params = {"page": page}
    return render(request, "booktest/show_area.html", params)


def areas(request):
    # 省市县页面
    return render(request, "booktest/pcc.html")


def find_areas(request, parentId):
    # 获取省市县
    if parentId:
        areas = AreaInfo.objects.filter(aParent__id=parentId)
    else:
        areas = AreaInfo.objects.filter(aParent=0)
    data = []
    for area in areas:
        data.append({"id": area.id, "atitle": area.atitle})
    return JsonResponse({"data": data})
