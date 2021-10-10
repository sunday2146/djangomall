from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
User = get_user_model()

# Create your models here.
from dadmin.models import BaseModel


class DmallFavorite(BaseModel):
    """用户收藏,通用
    """
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = '收藏'
        verbose_name_plural = verbose_name
        unique_together = ("owner", "content_type", "object_id")
        db_table = 'd_fav'

    def __str__(self):
        return str(self.object_id)


class DmallRate(BaseModel):
    # 评分系统
    SCORE_CHOICES = [
        (0, '0分'),
        (1, '1分'),
        (2, '2分'),
        (3 ,'3分'),
        (4, '4分'),
        (5, '5分'),
    ]
    score = models.SmallIntegerField(choices=SCORE_CHOICES, default=5, verbose_name="满意度评分")
    disabled = models.BooleanField('是否允许打分', default=True)

    class Meta:
        verbose_name = '评分'
        verbose_name_plural = verbose_name
        db_table = 'd_rate'
    
    def __str__(self) -> str:
        return str(self.num)


class DmallHotSearchWords(BaseModel):
    """
      热搜词
    """
    keywords = models.CharField( 
        max_length=20, 
        verbose_name="热搜词",
        help_text="热搜词")
    sort = models.PositiveSmallIntegerField(
        default=0, 
        verbose_name="排序",
        help_text="排序")

    class Meta:
        verbose_name = '热搜词'
        verbose_name_plural = verbose_name
        db_table = "d_hot_words"

    def __str__(self) -> str:
        return self.keywords