from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = "ticket"

urlpatterns = [
    path('', views.index, name='index'),
    path('account/login/', auth_views.LoginView.as_view(), name="login"),
    path('account/logout/',auth_views.LogoutView.as_view(), name="logout"),
    path('signup/',views.signup,name="signup"),
    path('book/', views.book, name='book'),
    path('transcaction/', views.tran, name='tran'),
    path('receipt/', views.receipt, name='receipt'),

]