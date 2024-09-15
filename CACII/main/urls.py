from django.urls import path
from . import views
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
    path("", views.index, name="index"),
    path("timeline/", views.timeline, name="timeline"),
    path("timeline/module-preview/", views.preview, name="preview"),
    path("timeline/module-content/", views.module, name="module"),
    path('chat/', views.chat, name='chat'),
    path('register_new/', views.register_new, name='register_new'),
    path('login/',views.login_view,name='login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('create_profile/', views.create_profile, name='create_profile'),
    path('profile/', views.profile_view, name='profile_view'),
]
