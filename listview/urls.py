from django.urls import path, include
from . import views
from .views import Delete


urlpatterns = [
    path('', views.index, name = "Home"),
    path('example/', views.example, name = "example"),
    # path('login/', views.login, name = "Login"),
    path('signup/', views.signup, name = "Signup"),
    path('approvals/', views.approvals, name = "approvals"),
    path('delete_record/', Delete.as_view(), name='delete-record'),
    path('delete_user/', views.delete_user, name='delete-user'),
    path('update_record/', views.editRecord, name = "Update"),
    path('upload_record/', views.upload, name = "Upload"),
    path('massmail', views.massmail, name = 'massmail'),
    path('create_user', views.createUser, name="create_user"),
    path('approve_user', views.approveUser, name="approve_user"),
    path('approve_new_user', views.approve_new_user, name="approve_new_user"),
    path('delete_new_user', views.delete_new_user, name="delete_new_user"),
    path('users/', views.users, name = "Users"),
    path('file/', views.open_files, name = "open_files"),
    path('dfile/', views.delete_files, name = "delete_files"),
    path('new_file/', views.new_upload, name = "new_upload"),
   
]