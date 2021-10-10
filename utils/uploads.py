from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings

'''
@File    :   uploads.py
@Time    :   2021/08/11 19:11:44
@Author  :   幸福关中 & 轻编程 
@Version :   1.0
@Contact :   baywanyun@qq.com
@Desc    :   富文本编辑方法以及与上传文件有关的方法
'''

@csrf_exempt
def upload_file(request):
    """ ckeditor5图片上传 """
    upload = request.FILES.get('upload')
    # print(upload)
    import os
    new_path = os.path.join(settings.MEDIA_ROOT, 'upload/', upload.name)
    # new_path = os.path.join(settings.MEDIA_ROOT, 'post', upload)
    with open(new_path, 'wb+') as destination:
        for chunk in upload.chunks():
            destination.write(chunk)

    filename = upload.name
    url = '/media/upload/' + filename
    retdata = { 'url': url, 
                'uploaded': '1',
                'fileName': filename }
    return JsonResponse(retdata)