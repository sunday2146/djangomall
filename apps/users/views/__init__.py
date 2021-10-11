from .views import DmallLoginView, DmallLogoutView, DmallRegisterCreateView, DmallAuthBackend
from .operate import (
    DmallAddressHasDefault, DmallFavoriteView, DmallSearchView, 
    DmallAddressCreateView, DmallAddressUpdateView, DmallAddressDeleteView,
    DmallFavoriteCreateView, DmallFavoriteDeleteView, UserInfoUpdateView
)
from .userinfo import (
    DmallUserInfoDetailView, DmallOwnerOrderInfoListView,
    DmallOwnerOrderInfoDetailView, DmallAddressListView, DmallFavoriteListView
)