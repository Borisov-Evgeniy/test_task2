from django.urls import path
from item.views import get_checkout_session_id, get_item_page, create_order, order_detail, item_list

urlpatterns = [
    path('', item_list, name='item_list'),
    path('buy/<int:item_id>/', get_checkout_session_id, name='get_checkout_session_id'),
    path('item/<int:item_id>/', get_item_page, name='get_item_page'),
    path('create_order/<int:item_id>/', create_order, name='create_order'),
    path('order/<int:order_id>/', order_detail, name='order_detail'),
]