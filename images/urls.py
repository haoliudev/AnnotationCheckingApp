from django.urls import path
from . import views

urlpatterns = [
    path('', views.gallery, name='gallery'),
    path('image/<str:pk>/', views.viewImg, name='image'),
    path('editlabel/<str:pk>/', views.editlabel, name='editlabel'),
    path('add/', views.addImg, name='add'),
    path('upload/', views.addFiles, name='uploadfile'),
    path('clearfiles/', views.clearfiles, name='clearfiles'),
    path('addlabel/', views.addLabel, name='addlabel'),
    path('bulkupload/', views.bulkUpload, name='bulkupload'),
    path('removeannotation/<str:pk>/', views.removeAnnotation, name='removeannotation'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),

   
]