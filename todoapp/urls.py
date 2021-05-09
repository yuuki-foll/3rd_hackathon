from django.contrib import admin
from django.urls import path, include
from .views import signupfunc, loginfunc, TodoList, TodoCreate, TodoDelete, logoutfunc, TodoDetail, TodoEdit, \
                    donefunc, sendemailfunc, TodoToday, TodoTomorrow, TodoFuture, sendtodofunc, sendtodotodayfunc

urlpatterns = [
    # path('signup/', TodoSignup.as_view(),name='signup'),
    path('signup/', signupfunc, name='signup'),
    path('login/', loginfunc, name='login'),
    path('list/', TodoList.as_view(), name='list'),
    path('detail/<int:pk>/', TodoDetail.as_view(), name='detail'), 
    path('create/', TodoCreate.as_view(), name='create'),
    path('edit/<int:pk>', TodoEdit.as_view(), name='edit'),       
    path('delete/<int:pk>', TodoDelete.as_view(), name='delete'),
    ####追加
    path('logout/', logoutfunc, name='logout'), #ログアウト画面
    path('done/<int:pk>', donefunc, name='done'),
    path('sendemail/',sendemailfunc, name='mail'),
    path('today/', TodoToday.as_view(), name='today'),      
    path('tomorrow/', TodoTomorrow.as_view(), name='tomorrow'),     
    path('future/', TodoFuture.as_view(), name='future'),
    path('sendtodo/',sendtodofunc, name='todo'),  #追加
    path('sendtodotoday/',sendtodotodayfunc, name='todotoday'), #追加       
    path('', loginfunc, name='login'),
]
