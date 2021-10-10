import json
from django.shortcuts import redirect, render
from django.views.generic import View
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from .import admin

class LoginView(View):
    # 前后端分离登录视图
    template_name = 'dadmin/login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class HasLoginRequired(LoginRequiredMixin):
    # 限制类登录才能访问
    login_url = '/users/login/'
    redirect_field_name = 'redirect_to'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({
                'code': 10010, 
                'login_url': self.get_login_url(),
                'message': '未登录,请登录后操作！'
                })
           
        return super().dispatch(request, *args, **kwargs)


class IndexView(View):
    # 前后端分离登录视图
    template_name = 'dadmin/index.html'

    def get(self, request, *args, **kwargs):
        
        context = dict(
            admin.admin_site.each_context(request),   # 站点信息
        )
        return render(request, self.template_name, context)
