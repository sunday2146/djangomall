from rest_framework_simplejwt.tokens import RefreshToken

'''
@File    :   get_token.py
@Time    :   2021/08/11 19:12:24
@Author  :   幸福关中 & 轻编程 
@Version :   1.0
@Contact :   baywanyun@qq.com
@Desc    :   手动获取token
'''

def get_tokens_for_user(user):
    # 手动返回令牌
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
