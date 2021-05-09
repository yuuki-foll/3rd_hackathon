from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView
from .models import TodoModel
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin # ログインしないとlistを見れないようにする
from django.forms import SelectDateWidget
from django.core.mail import send_mail
from django.http import HttpResponse
import datetime
# Create your views here.


class TodoList(LoginRequiredMixin,ListView): # LoginRequiredMixinを追加 setting.pyにlogin_url追加
    template_name = 'list.html'
    model = TodoModel

    # ユーザでフィルタかけたい
    def get_queryset(self):
        return TodoModel.objects.filter(user=self.request.user)

class TodoToday(LoginRequiredMixin,ListView): # LoginRequiredMixinを追加 setting.pyにlogin_url追加
    template_name = 'list_today.html'
    model = TodoModel
    today = datetime.date.today()
    # ユーザでフィルタかけたい
    def get_queryset(self):
        return TodoModel.objects.filter(user=self.request.user, created_date=self.today)


class TodoTomorrow(LoginRequiredMixin,ListView): # LoginRequiredMixinを追加 setting.pyにlogin_url追加
    template_name = 'list_tomorrow.html'
    model = TodoModel
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    # ユーザでフィルタかけたい
    def get_queryset(self):
        return TodoModel.objects.filter(user=self.request.user, created_date=self.tomorrow)


class TodoFuture(LoginRequiredMixin,ListView): # LoginRequiredMixinを追加 setting.pyにlogin_url追加
    template_name = 'list_future.html'
    model = TodoModel
    future = datetime.date.today() + datetime.timedelta(days=2)
    # ユーザでフィルタかけたい
    def get_queryset(self):
        return TodoModel.objects.filter(user=self.request.user, created_date__gte=self.future)

class TodoCreate(CreateView):
    template_name = 'create.html'
    model = TodoModel
    fields = ('title','text','created_date')
    success_url = reverse_lazy('today')

    # 日付を入力しやすくする
    def get_form(self):
        form = super(TodoCreate, self).get_form()
        form.fields['created_date'].widget = SelectDateWidget()
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TodoCreate, self).form_valid(form)

class TodoDelete(DeleteView):
    template_name = 'delete.html'
    model = TodoModel
    success_url = reverse_lazy('today')


class TodoDetail(DetailView):
    template_name = 'detail.html'
    model = TodoModel

class TodoEdit(UpdateView):
    template_name = 'edit.html'
    model = TodoModel
    fields = ('title', 'text', 'created_date')
    success_url = reverse_lazy('today')

    # 日付を入力しやすくする
    def get_form(self):
        form = super(TodoEdit, self).get_form()
        form.fields['created_date'].widget = SelectDateWidget()
        return form
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TodoEdit, self).form_valid(form)

def signupfunc(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = User.objects.create_user(username, email, password)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('mail')
            return redirect('today')
        except IntegrityError:
            return render(request, 'signup.html', {'error' : 'そのユーザ名は既に存在しています。'})

    return render(request, 'signup.html', {})

def loginfunc(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('today')

        else:
            return render(request, 'login.html', {'context' : 'ログインできません'})
    return render(request, 'login.html', {})

# 追加
def logoutfunc(request):
    logout(request)
    return redirect('login')

def donefunc(request, pk):
    do = get_object_or_404(TodoModel, pk=pk)
    do.delete()
    return redirect("today")

def sendemailfunc(request):
    user = request.user  # ログインユーザーを取得する
    """題名"""
    subject = 'todotoitoit'
    """本文"""
    message = user.username+"さん\n登録ありがとうございます。"
    """送信元メールアドレス"""
    from_email = "todo.toitoi@gmail.com"
    # send_mail(subject, message, from_email, recipient_list)
    user.email_user(subject, message, from_email)
    return redirect('today')

# 追加
def sendtodofunc(request):
    user = request.user  # ログインユーザーを取得する
    """題名"""
    subject = " thing to do"
    """本文"""
    text = ""
    for items in TodoModel.objects.all():
        if items.user == user:
            text = text +"☆"+str(items.title)+"   期日；"+str(items.created_date)+ "\n"
    message = user.username+"さん\nやるべきことが残っています！\n" + text

    """送信元メールアドレス"""
    from_email = "todo.toitoi@gmail.com"
    # send_mail(subject, message, from_email, recipient_list)
    user.email_user(subject, message, from_email)
    return redirect('today')

# 追加
def sendtodotodayfunc(request):
    user = request.user  # ログインユーザーを取得する
    """題名"""
    subject = "today's thing to do"
    """本文"""
    text = ""
    d_today = datetime.date.today() #今日の日付を取得
    for items in TodoModel.objects.all():
        if items.created_date == d_today and items.user == user:
            text = text +"☆"+str(items.title)+"   期日；"+str(items.created_date)+ "\n"
    message = user.username+"さん\n今日やるべきことです！\n" + text
    """送信元メールアドレス"""
    from_email = "todo.toitoi@gmail.com"
    # send_mail(subject, message, from_email, recipient_list)
    user.email_user(subject, message, from_email)
    return redirect('today')