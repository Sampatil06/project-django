from django.urls import path
from . import views

urlpatterns = [
    path('', views.signup, name='home'),  
    path('signup/', views.signup, name='signup'),
    path('chat/', views.chat, name='chat'),
    path('messages/<int:recipient_id>/', views.get_messages, name='get_messages'),
     path('login/', views.login_view, name='login'),
]

