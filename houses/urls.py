from django.urls import path
from . import views

app_name = 'houses'

urlpatterns = [
    # house urls for crud operations
    path('house/', views.house_list, name='house_list'), # <-- house list with infinite scroll
    path('house/add/', views.HouseCreate.as_view(), name='house_add'),
    path('house/<int:pk>/update/', views.HouseUpdate.as_view(), name='house_update'),
    path('house/<int:pk>/delete/', views.HouseDelete.as_view(), name='house_delete'),

    # ************** house detail ************** 
    path('house/<int:pk>/detail/', views.HouseDetail.as_view(), name='house_detail'), # create comment 
    path('house/<int:pk>/detail/<int:comment_pk>/update/', views.HouseUpdateComment.as_view(), name='house_update_comment'), # update comment 
    path('house/<int:pk>/detail/<int:comment_pk>/delete/', views.HouseDeleteComment.as_view(), name='house_delete_comment'), # delete comment 

]
