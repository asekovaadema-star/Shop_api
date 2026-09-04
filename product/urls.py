from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_create_list_api_view), 
    path('<int:id>', views.product_datail_api_view), 
    path('', views.category_create_list_api_view), 
    path('<int:id>', views.product_datail_api_view), 
    path('', views.review_create_list_api_view), 
    path('<int:id>', views.review_detail_api_view),
]