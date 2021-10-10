import base64
import json
from django.http import HttpResponse
from rest_framework.views import APIView
from captcha.views import CaptchaStore, captcha_image

# 参考代码：https://www.cnblogs.com/lyq-biu/p/10077820.html

class CaptchaAPIView(APIView):
    
    def get(self, request):
        hashkey = CaptchaStore.generate_key()
        try:
            #获取图片id
            id_ = CaptchaStore.objects.filter(hashkey=hashkey).first().id
            imgage = captcha_image(request, hashkey)
            #将图片转换为base64
            image_base = 'data:image/png;base64,%s' % base64.b64encode(imgage.content).decode('utf-8')
            json_data = json.dumps({"id": id_, "image_base": image_base })
            # 批量删除过期验证码
            CaptchaStore.remove_expired()
        except:
            json_data = None
        return HttpResponse(json_data, content_type="application/json")   
