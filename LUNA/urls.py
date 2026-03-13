"""
URL configuration for LUNA project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path, include
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('dailytask/', views.dailytask, name='dailytask'),
    path('expensetracker/', views.expensetracker, name='expensetracker'),
    path('taskmanager/', views.taskmanager, name='taskmanager'),
    path('complete-task/<int:task_id>/', views.complete_task, name='complete_task'),
    path('task-complete/<int:task_id>/', views.complete_taskmanager, name='complete_taskmanager'),
    path('update-daily-task/<int:task_id>/', views.update_daily_task, name='update_daily_task'),
    path('delete-daily-task/<int:task_id>/', views.delete_daily_task, name='delete_daily_task'),
    path('update-taskmanager/<int:task_id>/', views.update_taskmanager, name='update_taskmanager'),
    path('delete-taskmanager/<int:task_id>/', views.delete_taskmanager, name='delete_taskmanager'),
    path('update-expense/<int:expense_id>/', views.update_expense, name='update_expense'),
    path('delete-expense/<int:expense_id>/', views.delete_expense, name='delete_expense'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', views.signup, name='signup'),
]
