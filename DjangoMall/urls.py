"""DjangoMall URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.conf import settings
from django.conf.urls.static import static
from dadmin.admin import admin_site
from utils.uploads import upload_file
from .import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.IndexView.as_view(), name='index'),
    path('byadmin/', admin_site.urls),
    # path('dadmin/', include('dadmin.urls')),
    path('api-auth/', include('rest_framework.urls')),
    # path('api/', include('api.urls')),  # api接口
    path('frontapi/', include('api.frontapi.urls')),
    path('captcha/', include('captcha.urls')),
    path('uploads/', upload_file, name='uploads'),  # 富文本编辑器上传图片
    path('product/', include('product.urls')),
    path('users/', include('users.urls')),
    path('order/', include('order.urls'))
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)