'''
@File    :   byadmin.py
@Time    :   2021/08/19 15:29:13
@Author  :   幸福关中 & 轻编程 
@Version :   1.0
@Contact :   baywanyun@qq.com
@Desc    :   后台admin的配置文件，django默认为admin.py 自定义站点的为byadmin.py
'''

import csv
from django.contrib import admin
from django.http.response import HttpResponse
from django.utils.html import format_html
from django.urls import reverse
from django.contrib.auth.models import User, Group
from .admin import admin_site
from .import settings


class ExportCsvMixin:
    """ 导出csv """

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv', charset='GB2312')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(
            meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field)
                                  for field in field_names])

        return response

    export_as_csv.short_description = "导出CSV"


class BaseOwnerAdmin(admin.ModelAdmin, ExportCsvMixin):
    """
    所有管理配置的继承类：
    operate设置操作字段，已在BaseOwnerAdmin中集成，可以重写!
    添加到list_display中默认显示编辑和删除操作！
    注意:这里的删除操作是直接从数据库删除，谨慎操作！

    移动到回收站，可以用动作中的mark_delete操作执行
    """
    change_list_template = "dadmin/change_list.html"

    # list_display = ('operate',)
    exclude = ('owner', 'is_del')
    list_filter = ('is_show',)
    search_placeholder = ""

    def get_queryset(self, request):
        # 仅显示未被移动到回收站的内容
        qs = super(BaseOwnerAdmin, self).get_queryset(request)
        return qs.filter(is_del=settings.IS_DELETE)

    def save_model(self, request, obj, form, change):
        # 用来自动保存admin Model的owner字段
        obj.owner = request.user
        return super(BaseOwnerAdmin, self).save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        # 设置内联模型用户的值
        for form in formset.forms:
            form.instance.owner = request.user
        formset.save()

    #### 自定义动作 ####
    actions = ["mark_show", "mark_delete", "export_as_csv"]

    def mark_delete(self, request, queryset):
        # 移入移除回收站
        if queryset.filter(is_del=True):
            queryset.update(is_del=False)
        else:
            queryset.update(is_del=True)

    mark_delete.short_description = "移到回收站"

    def mark_show(self, request, queryset):
        # 批量显示隐藏
        if queryset.filter(is_show=True):
            queryset.update(is_show=False)
        else:
            queryset.update(is_show=True)

    mark_show.short_description = "批量显示隐藏操作"

    #### 自定义动作 END ####

    def operate(self, obj):
        # 自定义操作方法
        return format_html(
            '<a class="button1" href="{}">编辑</a> | <a class="button1" href="{}">删除</a>',
            reverse(f'byadmin:{obj._meta.app_label}_{obj._meta.model_name}_change', args=(
                obj.pk, )),
            reverse(f'byadmin:{obj._meta.app_label}_{obj._meta.model_name}_delete', args=(
                obj.pk, )),
        )

    operate.short_description = '操作'

    def change_view(self, request, object_id, form_url='', extra_context=None):
        # 详情视图
        extra_context = {}
        change_view = super().change_view(request, object_id, form_url, extra_context)
        extra_context['js'] = 'https://cdn.bootcdn.net/ajax/libs/jquery/3.6.0/jquery.js'
        # if 'content' in self.get_fields(request):
        #     print(extra_context['js'])
        return change_view

    def changelist_view(self, request, extra_context=None):
        # 列表视图, 添加search_placeholder = ""
        # 即可定义搜索框的值，也可以向列表页得传进任何数据
        search_placeholder = getattr(self, "search_placeholder", False)
        if search_placeholder:
            extra_context = extra_context or {}
            extra_context["search_placeholder"] = search_placeholder
        return super().changelist_view(request, extra_context=extra_context)

    class Media:
        css = {
            'all': ('dadmin/css/change_list.css',)
        }


class BaseOwnerStackInline(admin.StackedInline):
    # 重写StackedInline
    exclude = ('owner', 'is_del')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(BaseOwnerStackInline, self).save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        # 设置内联模型用户的值
        for form in formset.forms:
            form.instance.owner = request.user
        formset.save()

    actions = ["mark_delete"]

    def mark_delete(self, request, queryset):
        if queryset.filter(is_del=True):
            queryset.update(is_del=False)
        else:
            queryset.update(is_del=True)

    mark_delete.short_description = "移动所选至回收站"


class BaseOwnerTabularInline(admin.TabularInline, BaseOwnerStackInline):
    # 重写TabularInline
    pass


class UserAdmin(admin.ModelAdmin):
    '''用户管理 '''

    list_display = ('id', 'username', 'email')
    list_filter = ('username',)
    search_fields = ('username',)

    def save_model(self, request, obj, form, change):
        # 密码加密
        password = obj.password
        obj.set_password(password)
        obj.save()
        return super().save_model(request, obj, form, change)

admin_site.register(User, UserAdmin)



class GroupAdmin(admin.ModelAdmin):
    '''用户管理 '''

    list_display = ('id', 'name')
    list_filter = ('name',)
    search_fields = ('name',)


admin_site.register(Group, GroupAdmin)
