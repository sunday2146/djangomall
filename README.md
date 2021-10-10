# DjangoMall
一个用Django实现的商城系统,正在开发中....

![](https://images.gitee.com/uploads/images/2021/0829/222326_ce6be5a1_2333816.png "企业微信截图_20210829222306.png")

![输入图片说明](https://images.gitee.com/uploads/images/2021/0916/152617_10668fec_2333816.gif "计算属性，侦听器1.gif")

 
### **项目介绍** 

本项目将基于Django + drf + djangorestframework-simplejwt + vue + mysql构建，未来将实现PC端 + 微信小程序，因为PC端做了响应式设计，可以做到自适应常见的屏幕，所以H5端暂时不在考虑范围，后台第一个版本会沿用django admin，但对admin模块进行了继承与扩展，增加了一些本身项目的东西，后期将会把后台完全分离，做一个vue版的后台，权限基于RBAC设计，当然以上大部分功能都是构想，因为本项目正在开发中...，所以以上不可全信，也不可不信，开发过程中有可能会调整哦！

###  **你可以用本项目干什么？** 

1. 对于初学Django的伙伴来说，本项目中的代码可能涉及到了django的大部分知识，你可以Star随时阅读参考借鉴，或者【谨慎学习】！
2. django-admin系统的高级用法本项目即会都会涵盖，包含子类化、模板及后台数据自定义等方面，你可以Star随时阅读参考借鉴，或者【谨慎学习】！
3. 本项目将使用了DRF来编写前后端的所有接口，对于DRF的知识及用法你也可以在其中窥探一二，以及快捷用法！
4. 本项目还在进一步完善，使用价值有限，欢迎大佬点评指正！

### 如何使用？
1. 克隆本项目代码，或者直接下载！
```
git clone https://gitee.com/xingfugz/django-mall
```
2. 进入DjangoMall
```python
cd django-mall
```
3. 创建虚拟环境

> 创建虚拟环境有多种方法，这里只说用python自带的模块创建,其他方法按自己使用习惯即可！
```python
python -m venv venv
```
4. 激活虚拟环境
```html
win:    venv\Scripts\activate
linux:  . venv/bin/activate
```
5. 安装依赖
```
pip3 install -r requirements.txt
```
6. 创建sqlite数据库【开发用】
```
py manage.py migrate
```
数据库创建成功后，最好运行下以下命令
```
py manage.py makemigrations
py manage.py migrate
```
7. 创建超级用户
```
py manage.py createsuperuser
```
8. 启动项目
```
py manage.py runserver
```
- 后台url：127.0.0.1:8000/byadmin/
- 账号密码：你自己在第七步创建的

走完以上步骤应该可以正常在开发环境运行本项目，因为本项目正在开发，不适合部署，部署文档将在程序逐步完善之后编写！

 **欢迎对django感兴趣的朋友，关注添加交流，技术探讨，共同进步，获取更多Python及Django资料！** 

![关注作者公众号一起学习！](https://images.gitee.com/uploads/images/2021/1009/140443_750b72be_2333816.jpeg "扫码_搜索联合传播样式-白色版.jpg")