from django.contrib import admin
from dadmin.admin import admin_site
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count
# Register your models here.
from dadmin.byadmin import BaseOwnerAdmin
from .models import CategoryModel, ArticleModel


class CategoryModelAdmin(BaseOwnerAdmin):
    """
    分类管理配置
    operate设置操作字段，已在BaseOwnerAdmin中集成，可以重写!
    添加到list_display中默认显示编辑和删除操作！
    注意:这里的删除操作是直接从数据库删除，谨慎操作！

    移动到回收站，可以用动作中的操作执行
    """

    list_display = ('id', 'name', 'is_show', 'cate_icon',
                    'sort',  'add_date', 'operate')
    readonly_fields = ('cate_icon',)
    list_editable = ('is_show', 'sort')
    list_filter = ()
    # inlines = [
    #     Inline,
    # ]
    # raw_id_fields = ('',)
    search_fields = ('name',)
    # date_hierarchy = ''
    # ordering = ('',)
    search_placeholder = '请输入分类名称搜索'

    def cate_icon(self, obj):
        # 分类图标
        if obj.icon:
            return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
                url=obj.icon.url, width=32, height=32))
        else:
            return mark_safe('暂未上传')

    cate_icon.short_description = "分类图标"

    def operate(self, obj):
        # 继承并重写
        oper = super().operate(obj)
        ops = format_html(
            oper + f' | <a href="/byadmin/article/articlemodel/?category__name={obj.name}">查看文章</a>',)
        return ops

    operate.short_description = '操作'


class ArticleModelAdmin(BaseOwnerAdmin):
    '''文章列表及详情视图'''

    list_display = ('id', 'article_cover', 'title', 'category', 'is_banner',
                    'is_hot', 'is_top', 'add_date', 'operate')
    list_editable = ('is_hot', 'is_top',)
    list_filter = ('category__name',)
    # raw_id_fields = ('',)
    readonly_fields = ('article_cover',)
    search_fields = ('title', 'category__name')
    # date_hierarchy = ''
    # ordering = ('',)

    search_placeholder = "文章标题 or 分类名称 模糊搜索"
    fields = ('title', 'desc', 'category',
              ('cover', 'article_cover'),
              'content', ('is_banner', 'is_hot', 'is_top', ))

    def article_cover(self, obj):
        # 分类图标
        if obj.cover:
            return mark_safe('<img src="{url}" width="{width}" height="{height}" />'.format(
                url=obj.cover.url, width=100, height='auto'))
        else:
            return mark_safe('暂未上传')

    article_cover.short_description = "封面图"

    class Media:
        js = (
            'https://cdn.bootcdn.net/ajax/libs/jquery/3.6.0/jquery.js',
            'dadmin/ckeditor5/ckeditor.js',
            'dadmin/ckeditor5/translations/zh.js',
            'dadmin/ckeditor5/config.js',
        )


admin_site.register(CategoryModel, CategoryModelAdmin)
admin_site.register(ArticleModel, ArticleModelAdmin)
