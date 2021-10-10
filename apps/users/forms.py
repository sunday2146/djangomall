from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.utils.translation import gettext_lazy as _
# from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from django.contrib.contenttypes.models import ContentType
from users.models.operate import DmallFavorite
from users.views.userinfo import User


class DmallLoginForm(AuthenticationForm):
    """登录表单
    """
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 'class': 'input', 
        'placeholder': '请输入用户名'}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'input',
            'placeholder': '请输入密码'}),
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists() or User.objects.filter(email=username).exists():
            pass
        else:
            raise ValidationError("该用户尚未注册！")
        return username

    def clean_password(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password) 
        if user is not None:
            pass
        else:
            raise ValidationError("您输入的密码错误！")
        return password


class DmallRegisterForm(forms.ModelForm):
    """ 注册表单 """
    email = forms.EmailField(label="邮箱", widget=forms.EmailInput(attrs={
        'class': 'input', 'placeholder': '请输入邮箱地址'
    }))
    username = forms.CharField(label="用户名", widget=forms.TextInput(attrs={
        'class': 'input', 'placeholder': '请输入用户名'
    }))
    password = forms.CharField(label="密码", widget=forms.PasswordInput(attrs={
        'class': 'input', 'placeholder': '请输入密码'
    }))

    class Meta:
        model = User
        fields = ('email', 'username', 'password')
    
    def clean_email(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            raise ValidationError("该邮箱地址已经存在，请更换未注册邮箱！")
        return email


class DmallFavoriteForm(forms.ModelForm):
    """Form definition for DmallFavorite."""

    class Meta:
        """Meta definition for DmallFavoriteform."""

        model = DmallFavorite
        exclude = ('owner', 'is_show', 'content_type')