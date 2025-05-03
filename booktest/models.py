from django.db import models

# Create your models here.


class BookInfo(models.Model):
    """图书模型"""
    # 图书名 db_column数据库字段
    #btitle = models.CharField(max_length=20, db_column="title")
    btitle = models.CharField(max_length=20)
    # 出版日期
    bpub_date = models.DateField()
    # 阅读量
    bread = models.IntegerField(default=0)
    # 评论量
    bcomment = models.IntegerField(default=0)
    # 删除标记
    isDelete = models.BooleanField(default=False)

    # django默认生成的表明是 应用名小写_模型类小写 如果应用名改变后 将找不到对应的表  在模型类中创建一个元选项Meta
    # 指定表名
    class Meta(object):
        db_table = "bookinfo"


class HeroInfo(models.Model):
    """英雄模型"""
    # 英雄名
    hname = models.CharField(max_length=20)
    # 性别
    hgender = models.BooleanField(default=False)
    # 备注
    hcomment = models.CharField(max_length=255)
    # 删除标记
    isDelete = models.BooleanField(default=False)
    #关系属性
    hbook = models.ForeignKey("BookInfo", on_delete=models.CASCADE)

    # django默认生成的表明是 应用名小写_模型类小写 如果应用名改变后 将找不到对应的表  在模型类中创建一个元选项Meta
    # 指定表名 指定之后 表明不再依赖于应用名
    class Meta(object):
        db_table = "heroinfo"


class AreaInfo(models.Model):
    """地区模型表"""

    # 名称
    atitle = models.CharField(max_length=20, verbose_name="标题") # verbose_name指定页面上表格头上显示什么
    # 自关联属性
    aParent = models.ForeignKey("self", on_delete=models.DO_NOTHING, null=True, blank=True)

    atitle.admin_order_field = 'atitle'     #字段排序

    def __str__(self):
        return self.atitle

    def parent(self):
        if self.aParent is None:
            return ""
        return self.aParent.atitle
    parent.short_description = "父级地区"       # 方法也可以显示在页面上，在admin文件的列表中写上方法名就可以，方法指定表头名使用 方法.short_description

    class Meta(object):
        db_table = "areainfo"


class Pictest(models.Model):
    """上传文件"""
    gpic = models.ImageField(upload_to="booktest")

    class Meta(object):
        db_table = "pictest"