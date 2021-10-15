'''
@File    :   conf.py
@Time    :   2021/10/12 17:18:49
@Author  :   幸福关中 & 轻编程 
@Version :   1.0
@Contact :   baywanyun@qq.com
@Desc    :   相关配置文件
'''
from DjangoMall.settings import alipay_private_key_path, alipay_public_key_path


################### 支付宝支付配置 #######################

alipay_appid = "2021000116697536"
return_url = "http://mall.lotdoc.cn/order/alipay/"
notify_url= "http://mall.lotdoc.cn/order/alipay/"   # 可选, 不填则使用默认notify url
alipay_debug=True,  # 默认False
alipay_private_key_path = alipay_private_key_path
alipay_public_key_path = alipay_public_key_path

################### 支付宝支付配置 END #######################