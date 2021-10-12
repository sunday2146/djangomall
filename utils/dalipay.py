'''
@File    :   alipay.py
@Time    :   2021/09/22 19:17:57
@Author  :   幸福关中 & 轻编程 
@Version :   1.0
@Contact :   baywanyun@qq.com
@Desc    :   感谢该开源项目：https://github.com/fzlee/alipay,本项目支付宝支付依赖该项目
'''

from alipay import AliPay, DCAliPay, ISVAliPay
from alipay.utils import AliPayConfig
# from DjangoMall.settings import alipay_private_key_path, alipay_public_key_path
from DjangoMall.conf import alipay_private_key_path, alipay_public_key_path, alipay_appid, alipay_debug, notify_url

app_private_key_string = open(alipay_private_key_path).read()
alipay_public_key_string = open(alipay_public_key_path).read()
# print(app_private_key_string)
app_private_key_string == """
    -----BEGIN RSA PRIVATE KEY-----
    base64 encoded content
    -----END RSA PRIVATE KEY-----
"""
# print(app_private_key_string)
alipay_public_key_string == """
    -----BEGIN PUBLIC KEY-----
    base64 encoded content
    -----END PUBLIC KEY-----
"""
# print(alipay_public_key_string)
def Alipay():
    alipay = AliPay(
        appid=alipay_appid,
        app_notify_url=notify_url,  # 默认回调url
        app_private_key_string=app_private_key_string,
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        alipay_public_key_string=alipay_public_key_string,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=alipay_debug,  # 默认False
        verbose=False,  # 输出调试数据
        config=AliPayConfig(timeout=15)  # 可选, 请求超时时间
    )
    return alipay

"""
dc_alipay = DCAliPay(
    appid="appid",
    app_notify_url="http://example.com/app_notify_url",
    app_private_key_string=app_private_key_string,
    app_public_key_cert_string=app_public_key_cert_string,
    alipay_public_key_cert_string=alipay_public_key_cert_string,
    alipay_root_cert_string=alipay_root_cert_string
)


# 如果您没有听说过ISV， 那么以下部分不用看了
# app_auth_code或app_auth_token二者需要填入一个
isv_alipay = ISVAliPay(
    appid="",
    app_notify_url=None,  # 默认回调url
    app_private_key_srting="",
    # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
    alipay_public_key_string="",
    sign_type="RSA", # RSA or RSA2
    debug=False,  # False by default,
    app_auth_code=None,
    app_auth_token=None
)
"""