from django.urls import path
from .import views

app_name = "dadmin"

urlpatterns = [
    path('login/', views.LoginView.as_view(), name="login"),
]

admin_urls = [
    path('myview/', views.IndexView.as_view(), name="myview")
]