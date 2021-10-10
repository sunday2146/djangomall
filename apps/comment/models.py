from users.models.operate import DmallFavorite
from django.db import models

# Create your models here.
from users.models import DmallFavorite, DmallRate


class DmallComment(DmallFavorite):
    # 评论
    rate = models.OneToOneField(DmallRate, on_delete=models.CASCADE, verbose_name="评分")
    content = models.TextField('评论内容')
    imgs = models.ImageField(max_length=300,upload_to="comment/",null=True, blank=True,verbose_name="评论图")
    is_anonymous = models.BooleanField(default=False,verbose_name="是否匿名评价")

    class Meta:
        verbose_name = "评论"
        verbose_name_plural = verbose_name
        db_table = "d_comment"

    def __str__(self):
        return self.content