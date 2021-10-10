from django.db.models import Q
from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import View, CreateView
from django.contrib.auth.backends import ModelBackend
# Create your views here.
from users.forms import DmallLoginForm, DmallRegisterForm
from users.views.userinfo import User


class DmallAuthBackend(ModelBackend):
    """ 自定义用户验证，继承ModelBackend, 重写authenticate方法
    ModelBackend 类实际是django继承BaseBackend实现的验证登录后端，
    我们这里使用的是django自带的验证后端，那最好的做法就是扩展重写该类
    """
    def authenticate(self, request, username=None, password=None):
        # Check the username/password and return a user.
        try:
            user = User.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None


class DmallLoginView(LoginView):
    # 登录视图
    form_class = DmallLoginForm
    template_name = 'users/login.html'
    redirect_authenticated_user = True   # 登录之后不允许访问

    def get_success_url(self) -> str:
        # 重写登陆成功跳转逻辑
        red_url = super().get_success_url()
        if red_url == "/accounts/profile/":
            red_url = "/"
            return red_url
        return red_url
    

class DmallRegisterCreateView(CreateView):
    # 注册视图
    # model = User
    template_name = 'users/register.html'
    # fields = ('email', 'username', 'password')
    form_class = DmallRegisterForm
    success_url = "/users/login/"

    def form_valid(self, form):
        new_user = form.save(commit=False)                        # 暂存
        new_user.set_password(form.cleaned_data.get('password'))  # 密码加密
        new_user.save()                                           # 保存
        return super().form_valid(form)


class DmallLogoutView(LogoutView):
    # 退出登录
    template_name = 'users/logout.html'
    redirect_authenticated_user = True


class DmallUserView():
    pass