from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('history/', views.history, name='history'),
  path('history/<int:vote_id>/', views.history_change_vote, name='change_vote'),
  path('accounts/login/', auth_views.LoginView.as_view(template_name='admin/login.html')),
]
