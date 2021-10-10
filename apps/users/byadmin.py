from django.contrib import admin
from dadmin.admin import admin_site
from dadmin.byadmin import BaseOwnerAdmin
from django.utils.safestring import mark_safe
from dadmin.models import Banner, ADSpace
from .inbyadmin import ADContentStackedInline
from .models import DmallFavorite, DmallAddress, UserInfo


class BannerAdmin(BaseOwnerAdmin):
    """[Banner]
    轮播图后台管理
    """
    list_display = ('id', 'banner_image', 'url', 'desc', 'sort', 'operate')
    readonly_fields = ('banner_image',)

    def banner_image(self, obj):
        # 分类图标
        if obj.img:
            return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
                url=obj.img.url, width='auto', height=100))
        else:
            return mark_safe('暂未上传')

    banner_image.short_description = "轮播图"

admin_site.register(Banner, BannerAdmin)


class ADSpaceAdmin(BaseOwnerAdmin):
    """[ADSpace]
    广告位后台管理
    """
    list_display = ('id', 'name', 'is_show', 'operate')
    inlines = [
        ADContentStackedInline
    ]

admin_site.register(ADSpace, ADSpaceAdmin)


class DmallFavoriteAdmin(BaseOwnerAdmin):
    """[DmallFavorite]
    商品收藏后台管理
    """
    list_display = ('id', 'content_type', 'object_id', 'owner', 'is_show', 'is_del')
    list_filter = ('owner',)

admin_site.register(DmallFavorite, DmallFavoriteAdmin)


class DmallAddressAdmin(BaseOwnerAdmin):
    '''Admin View for '''

    list_display = ('id', 'province', 'city', 'address', 'signer_name', 'signer_mobile', 'email',)


admin_site.register(DmallAddress, DmallAddressAdmin)


class UserInfoAdmin(BaseOwnerAdmin):

    list_display = ('owner', 'mobile', 'nickname', 'avatar', 'signature', )
    # list_filter = ('user', )

admin_site.register(UserInfo, UserInfoAdmin)