from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:info_id>/', views.detail, name='detail'),
    path('answer/create/<int:info_id>/', views.answer_create, name='answer_create'),
    path('info/create/', views.info_create, name='info_create'),
    path('answer/modify/<int:answer_id>/', views.answer_modify, name='answer_modify'),
    path('answer/delete/<int:answer_id>/', views.answer_delete, name='answer_delete'),
    ]