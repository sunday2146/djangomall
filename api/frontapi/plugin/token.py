'''
@File    :   token.py
@Time    :   2021/09/10 14:06:22
@Author  :   幸福关中 & 轻编程 
@Version :   1.0
@Contact :   baywanyun@qq.com
@Desc    :   自定义登录的视图方法，增加了验证码
'''

from django.utils import timezone
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from utils.get_token import get_tokens_for_user
from captcha.fields import CaptchaStore


class DmallTokenObtainPairSerializer(TokenObtainPairSerializer):
    # 登录接口
    captcha = serializers.CharField(max_length=4, required=True,
                                    trim_whitespace=True, min_length=4,
                                    error_messages={
                                        "max_length": "图片验证码仅允许4位",
                                        "min_length": "图片验证码仅允许4位",
                                        "required": "请输入图片验证码"
                                    }, help_text="图片验证码")
    imgcode_id = serializers.CharField(required=True, write_only=True, help_text="图片验证码id")
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['captcha'] = user.captcha
        token['imgcode_id'] = user.imgcode_id
        return token
    
    def validate_captcha(self, captcha):
        # 验证码验证
        try:
            captcha = captcha.lower()
        except:
            raise serializers.ValidationError("验证码错误")
        img_code = CaptchaStore.objects.filter(id = int(self.initial_data['imgcode_id'])).first()
        if img_code and timezone.now() > img_code.expiration:
            raise serializers.ValidationError("图片验证码过期")
        else:
            if img_code and img_code.response == captcha:
                pass
            else:
                raise serializers.ValidationError("验证码错误")
    
    def validate(self, attrs):
        # 删除验证码
        del attrs['captcha']
        del attrs['imgcode_id']
        authenticate_kwargs = {
            'username': attrs['username'],
            'password': attrs['password'],
        }
        # 验证当前登录用户
        self.user = authenticate(**authenticate_kwargs)
        if self.user is None:
            raise serializers.ValidationError('账号或密码不正确')
        # 登录成功返回token信息
        token = get_tokens_for_user(self.user)
        return token


# views
from rest_framework_simplejwt.views import TokenObtainPairView

class DmallTokenObtainPairView(TokenObtainPairView):
    # 登录成功返回token
    serializer_class = DmallTokenObtainPairSerializer
