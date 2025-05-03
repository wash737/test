from django.contrib import admin
from .models import BookInfo, HeroInfo, AreaInfo, Pictest

# Register your models here.
# 注册模型类 可以在后台显示
#自定义模型管理类 用来自定义页面上可以显示什么内容


#class BookInfoAdmin(admin.ModelAdmin):
    #"""图书模型管理类"""
    #list_display = ["id", "btitle", "bpub_date"]


#class HeroInfoAdmin(admin.ModelAdmin):
    #"""英雄模型管理类"""
    #list_display = ["id", "hname", "hgender", "hcommer", "hbook"]

# 在一端显示多端的数据
class AreaStackedInline(admin.StackedInline):
    # 写多类
    model = AreaInfo

# 在一端显示多端的数据
class AreaTabularInline(admin.TabularInline):
    # 写多类
    model = AreaInfo


class AreaInfoAdmin(admin.ModelAdmin):  # 这里定义好之后，需要在注册后面加上此类名
    """地区模型管理类"""
    list_display = ["id", "atitle", "aParent_id", "parent"]       # 控制页面上显示什么
    list_per_page = 10                                  # 指定每页显示10条
    actions_on_top = False                              # 关闭页面上的动作下拉选项
    actions_on_bottom = True                            # 给下面添加一个动作下拉选项
    list_filter = ["atitle"]                            # 根据哪些数据进行过滤
    search_fields = ["atitle"]                          # 列表页上方的搜索框 根据哪些字段进行搜索
    #fields = ["aParent", "atitle"]                      # 修改页面  调整字段显示的顺序 fields跟fieldsets只能用一个

    # 分组
    fieldsets = (
        ("基本", {"fields": ["atitle"]}),
        ("高级", {"fields": ["aParent"]})
    )

    #inlines = [AreaStackedInline]
    inlines = [AreaTabularInline]


# 注册模型类 让django后台管理系统给你生成对应模型（表）的页面
admin.site.register(BookInfo)
admin.site.register(HeroInfo)
admin.site.register(AreaInfo, AreaInfoAdmin)
admin.site.register(Pictest)
