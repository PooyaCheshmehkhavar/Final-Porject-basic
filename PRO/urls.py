from django.urls import path
from .views import *

app_name = 'PRO'

urlpatterns = [
    path("", Index.as_view(), name="index"),
    path('home/', Home.as_view(), name='home'),
    path("admin/", Admin.as_view(), name="admin"),
    path('courses/', Courses.as_view(), name='courses'),
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path("logout/", Logout.as_view(), name="logout"),
]