from django.contrib import admin
from django.urls import path
from main import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from main.views import TaskViewSet

router = DefaultRouter()
router.register(r'Task', TaskViewSet, basename='task')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('create_task/', views.create_task, name='create_task'),
    path('api/', include(router.urls)),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('allauth.urls')),
]
