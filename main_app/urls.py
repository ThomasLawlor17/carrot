
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),

    # Account routes
    path('account/signup/', views.signup, name='signup'),
    path('account/<int:user_id>/', views.account_detail, name='account_detail'),

    # Run routes
    path('runs/', views.runs_index, name='runs_index'),
    path('runs/<int:run_id>/', views.run_detail, name='run_detail'),
    path('runs/create/', views.RunCreate.as_view(), name='run_create'),
    # To be changed later
    # path('runs/new/', views.run_new, name='run_new'),
    # path('runs/create/', views.run_create, name='run_create'),
    path('runs/<int:run_id>/add_image', views.add_image, name='add_image'),
    path('runs/<int:pk>/update/', views.RunUpdate.as_view(), name='run_update'),
    path('runs/<int:pk>/delete/', views.RunDelete.as_view(), name='run_delete'),
    path('runs/<int:run_id>/add_comment/', views.add_comment, name='add_comment'),
    # path('runs/<int:run_id>/<int:pk>/update/', views.CommentUpdate.as_view(), name='comment_update'),
    # path('runs/<int:run_id>/<int:pk>/delete/', views.CommentDelete.as_view(), name='comment_delete'),
    path('runs/<int:run_id>/assoc_gear/<int:gear_id>/', views.assoc_gear, name='assoc_gear'),
    path('runs/<int:run_id>/rmv_gear/<int:gear_id>/', views.rmv_gear, name='rmv_gear'),

    # Gear Routes
    path('gear/', views.gear_index, name='gear_index'),
    path('gear/<int:pk>/', views.GearDetail.as_view(), name='gear_detail'),
    path('gear/create/', views.GearCreate.as_view(), name='gear_create'),
    path('gear/<int:pk>/update/', views.GearUpdate.as_view(), name='gear_update'),
    path('gear/<int:pk>/delete/', views.GearDelete.as_view(), name='gear_delete'),
]