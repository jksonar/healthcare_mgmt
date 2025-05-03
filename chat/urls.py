from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_list, name='chat_list'),
    path('start/', views.start_chat, name='start_chat'),
    path('with/<int:user_id>/', views.chat_detail, name='chat_detail'),
]
