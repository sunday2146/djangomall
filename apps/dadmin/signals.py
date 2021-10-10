from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
User = get_user_model


@receiver(post_save, sender=User)
def create_veuser(sender, instance=None, created=False, **kwargs):
    # 用户注册时自动将密码转为密文
    if created:
        password = instance.password
        instance.set_password(password)
        instance.save()