from django.urls import path
from channel.views import homepage, signup, loginpage, logoutpage ,index

urlpatterns = [
    path('',index,name='home'),
    path('group/<str:groupname>/',homepage,name='homepage'),
    path('signup/',signup,name='signup'),
    path('login/',loginpage,name='login'),
    path('logout/',logoutpage,name='logout')
]
