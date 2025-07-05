from django.contrib import admin
from django.urls import path
from blog.views import home
from blog.views import (
    register, user_login,
    create_post, list_posts, post_detail, add_comment,
    like_post, edit_post, delete_post
)

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('api/register/', register),
    path('api/login/', user_login),
    path('api/create-post/', create_post),
    path('api/posts/', list_posts),
    path('api/post/<int:post_id>/', post_detail),
    path('api/post/<int:post_id>/comment/', add_comment),
    path('api/post/<int:post_id>/like/', like_post),
    path('api/post/<int:post_id>/edit/', edit_post),
    path('api/post/<int:post_id>/delete/', delete_post),
]