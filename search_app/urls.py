from django.urls import path 
from . import views 
from django.contrib.auth import views as auth_views
from . import views
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
from .views import SignUpView


app_name = 'search_app'


urlpatterns = [ 
    path('', lambda request: redirect('auth/login')),
    path('auth/signup/', SignUpView.as_view(), name="signup"),
    path('auth/login/', views.LoginView.as_view(), name='login'),
    path('auth/logout/', auth_views.LogoutView.as_view(next_page='search_app:login'), name='logout'),
    path('book/', views.search_book_list_view, name='search_book_list'),
    path('book/new/', views.book_create, name='book_create'), 
    path('book/<int:pk>/', views.book_detail, name='book_detail'), 
    path('book/<int:pk>/edit/', views.book_update, name='book_update'), 
    path('book/<int:pk>/delete', views.book_delete, name='book_delete'), 
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)