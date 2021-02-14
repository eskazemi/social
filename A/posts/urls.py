from django.urls import path
from . import views

app_name='posts'

urlpatterns=[
    path('',views.all_posts,name='all_posts'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/',views.detail_post,name='detail_post'),
    path('addpost/<int:user_id>/',views.add_post,name="add_post"),
    path('post_delete/<int:user_id>/<int:post_id>/',views.post_delete,name="post_delete"),
    path('post_edit/<int:user_id>/<int:post_id>/',views.post_edit,name="post_edit"),
    path('add_reply/<int:post_id>/<int:comment_id>/',views.add_reply,name="add_reply"),
]