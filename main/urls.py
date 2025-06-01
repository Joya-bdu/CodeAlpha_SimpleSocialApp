# main/urls.py অথবা socialapp/urls.py (যেখানেই তোমার app urls সংযুক্ত আছে)
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('post/create/', views.post_create, name='post_create'),  # ✅ এটি ঠিক আছে
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('profile/', views.profile_view, name='my_profile'),
    path('profile/<int:user_id>/', views.profile_view, name='profile'),
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
]

