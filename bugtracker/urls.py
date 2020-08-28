"""bugtracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from homepage import views

urlpatterns = [
    path('', views.index, name='home'),
    path('new_ticket/', views.add_ticket),
    path('ticket_view/<int:ticket_id>/', views.ticket_view, name='ticketV'),
    path('user_view/<int:user_id>/', views.user_view, name='userV'),
    path('edit_ticket/<int:ticket_id>/', views.edit_ticket),
    path('assign_ticket/<int:ticket_id>/', views.assign_ticket),
    path('complete_ticket/<int:ticket_id>/', views.complete_ticket),
    path('invalid_ticket/<int:ticket_id>/', views.invalid_ticket),
    path('return_ticket/<int:ticket_id>/', views.return_ticket),
    path('reopen_ticket/<int:ticket_id>/', views.reopen_ticket),
    path('login/', views.login_view),
    path('logout/', views.logout_view),
    path('admin/', admin.site.urls),
]
