from django.urls import path

from pic_board import views


urlpatterns = [
    path('create/', views.PicPostCreateApiView.as_view(), name='create_post'),
    path('edit/<int:pk>/', views.PicPostRetrieveUpdateDestroyApiView.as_view(), name='edit_post'),
    path('post-reaction/<int:pk>/', views.LikePostCreateListApiView.as_view(), name='like_post'),
    path('post-comment/<int:post_id>/', views.CommentPostApiView.as_view(), name='add_top_level_comment'),
    path('post-comment/<int:post_id>/<int:parent_comment_id>/', views.CommentPostApiView.as_view(), name='add_reply_to_comment'),
    path('delete-comment/<int:pk>/', views.CommentPostDestroyApiView.as_view(), name='delete_comment'),
    path('delete-like/<int:pk>/', views.LikePostDestroyApiView.as_view(), name='unlike_post'),
    path('post-feed/', views.PostFeedListApiView.as_view(), name='feeds'),
]