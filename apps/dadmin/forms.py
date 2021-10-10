from django import forms
from django.contrib.auth.forms import AuthenticationForm
from captcha.fields import CaptchaField, CaptchaTextInput
from dadmin.widget import CKEditorWidget


class CaptchaCodeInput(CaptchaTextInput):
    # 验证码表单小部件重写
    template_name = "dadmin/widgets/captcha.html"


class DadminAuthenticationForm(AuthenticationForm):
    captcha = CaptchaField(label='验证码', widget=CaptchaCodeInput(attrs={'class': 'input'}))
