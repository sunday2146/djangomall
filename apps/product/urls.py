from django.urls import path
from .import views


app_name = "product"

urlpatterns = [
    path('category/', views.ProductCategoryListView.as_view(), name="categories"),
    path('category/<int:pk>/', views.ProductCategoryDetailView.as_view(), name="category-detail"),
    path('product/<int:pk>/', views.ProductSPUDetailView.as_view(), name="product-detail"),
    path('product/<int:pk>/json/', views.ProductSPUDetailViewJson.as_view(), name='product-detail-json')
]