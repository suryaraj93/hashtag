from .views import Logout, Userview, Login
from django.urls import path

urlpatterns = [

    path('register/', Userview.as_view()),
    path('login/', Login.as_view()),
    path('logout/', Logout.as_view())

]
