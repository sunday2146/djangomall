'''
@File    :   admin.py
@Time    :   2021/08/19 15:28:22
@Author  :   幸福关中 & 轻编程 
@Version :   1.0
@Contact :   baywanyun@qq.com
@Desc    :   子类化Django admin 自定义自己的后台管理站点
'''

from django.contrib import admin
from django.utils.translation import gettext as _, gettext_lazy
from django.views.decorators.cache import never_cache

# Register your models here.
from .forms import DadminAuthenticationForm


class DadminSite(admin.AdminSite):
    # Text to put at the end of each page's <title>.
    site_title = gettext_lazy('DjangoMall site admin')

    # Text to put in each page's <h1>.
    site_header = gettext_lazy('DjanaoMall 管理')

    # Text to put at the top of the admin index page.
    index_title = gettext_lazy('Site administration')

    login_form = DadminAuthenticationForm
    login_template = "dadmin/login.html"
    index_template = 'dadmin/index.html'

    def get_urls(self):
        urls = super().get_urls()
        from dadmin.urls import admin_urls
        admin_urls = admin_urls
        return admin_urls + urls

    def get_app_list(self, request):
        # 重写侧边栏，模仿原有数据结构添加自定义数据
        app_list = super().get_app_list(request)
        dadmin_sidebar_dict = {
            'name': '控制台',
            'app_label': 'home',
            'app_url': '/byadmin/',
            'has_module_perms': True,
            'models': [
                {
                    'name': '站点管理', 'object_name': 'Home',
                    'perms': {'add': True, 'change': True, 'delete': True, 'view': True},
                    'admin_url': '/byadmin/',
                    # 'add_url': '/byadmin/auth/user/add/',
                    'view_only': False
                },
                # {
                #     'name': '组', 'object_name': 'Group',
                #     'perms': {'add': True, 'change': True, 'delete': True, 'view': True},
                #     'admin_url': '/byadmin/auth/group/',
                #     'add_url': '/byadmin/auth/group/add/',
                #     'view_only': False
                #     }
            ]
        }
        app_list.insert(0, dadmin_sidebar_dict)
        return app_list

    @never_cache
    def index(self, request, extra_context=None):
        """
        继承admin index向index添加数据
        """
        extra_context = {'ceshi': 'ceshi'}
        index_template = super().index(request, extra_context=extra_context)
        return index_template


admin_site = DadminSite(name='byadmin')

# 全局禁用删除
# admin_site.disable_action('delete_selected')
