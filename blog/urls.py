from .views import register_api, login, EnquireListAPiView
from django.urls import path, include
from rest_framework.authtoken import views
urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token),
    path('register/', register_api, name='register'),
    path('login/', login, name='login'),
    path('enquiry/list/<str:status>', EnquireListAPiView.as_view(), name='enquiry_list')

]