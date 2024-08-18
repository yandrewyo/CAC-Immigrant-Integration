from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("timeline/", views.timeline, name="timeline"),
    path("about/", views.about, name="about"),
    path("profile/", views.profile, name="profile"),
    path("timeline/module-preview/", views.preview, name="preview"),
    path("timeline/module-content/", views.module, name="module"),
    # path('chat/', views.chat_view, name='chat')
]
