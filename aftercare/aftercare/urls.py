from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from tracker.views import home_view

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('', include('tracker.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # login, logout
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
]
