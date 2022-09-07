"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from session import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('tune/all/<int:page>/', views.tunes_all, name="tunes_all"),
    path('tune/<int:tune_id>/', views.tune_detail, name='tune_detail'),
    path('session/all/', views.full_yt_session_list, name='full_yt_session_list'),
    path('session/<int:session_id>/', views.session_detail, name='session_detail'),
    path('session/add/', views.session_add, name='session_add'),
    path('session/<int:session_id>/edit', views.session_edit, name='session_edit'),
    path('session/session-played-group/add', views.session_add_played_group, name="session_add_played_group"),
    path('session/session-played-group/<int:played_tune_group_id>/edit', views.session_edit_played_group, name="session_edit_played_group"),
    path('session/session-played-group/<int:played_tune_group_id>/add', views.session_add_played_tune, name="session_add_played_tune"),    
    path('session/session-played-group/<int:played_tune_group_id>/delete', views.session_delete_played_group, name="session_delete_played_group"),
    path('nameyertune/all/', views.nameyertune_all, name='nameyertune_all'),
    path('youtube_loop_test2/', views.youtube_loop_test2, name='youtube_loop_test2'),
    path('adminlinks/', views.admin_links, name='admin_links'),
    path('adminlinks/sessionjson/', views.session_json, name="session_json"),
    
    # Testing Paths
    path('testing/', views.testing_path, name='testing_path')
]
