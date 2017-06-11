from django.shortcuts import render, get_object_or_404

# Create your views here.

from .models import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django import forms
from django.urls import reverse
import logging
logging.basicConfig(level=1)

def index(request):
    return HttpResponseRedirect(reverse('app:login'))

def student(request):
    book_list = Book.objects.all()
    has_borrow = Borrow.objects.filter(student_id=request.session['id'])
    return render(request, 'app/student.html', {'book_list': book_list, 'has_borrow': has_borrow})

def detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    borrowed = Borrow.objects.filter(student_id=request.session['id'], book_id=book_id).exists()
    context = {
        'book': book,
        "borrowed": borrowed # true / false
    }
    return render(request, 'app/detail.html', context)

def borrow(request, book_id): #数量判断留给客户端
    if Borrow.objects.filter(student_id=request.session['id'], book_id=book_id).exists():
        return HttpResponse("Exist")
    student = Student.objects.get(id=request.session['id'])
    book = Book.objects.get(id=book_id)
    Borrow.objects.create(student = student,book = book)
    book.bcount -= 1
    book.save()
    borrow = Borrow.objects.filter(student_id=request.session['id'])
    return HttpResponseRedirect(reverse('app:student'))

def return_book(request, book_id):
    Borrow.objects.get(student_id=request.session['id'],book_id=book_id).delete()
    book = Book.objects.get(id=book_id)
    book.bcount += 1
    book.save()
    borrow = Borrow.objects.filter(student_id=request.session['id'])
    return HttpResponseRedirect(reverse('app:student'))

def book_type(request, type_id):
    book_list = Book.objects.filter(btype_id=type_id)
    return render(request, 'app/student.html', {'book_list': book_list})

def admin_book_type(request, type_id):
    book_list = Book.objects.filter(btype_id=type_id)
    return render(request, 'app/admin_book_list.html', {'book_list': book_list})

IDENTITY = (
    ('student', '学生'),
    ('admin', '管理员'),
)

class LoginInfo(forms.Form):
    userid = forms.IntegerField(
        label='登陆名',
        widget=forms.TextInput(attrs={
            'class': 'text',
            'autofocus': 'true',
            'title': '请输入id号'
        })
    )
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(attrs={
            'class': 'text',
            'title': '请输入密码'
        })
    )
    identity = forms.ChoiceField(
        label='',
        widget=forms.RadioSelect(attrs={
            'id': 'radio',
            'class': 'text'
        }),
        choices=IDENTITY
    )

def login(request):
    if request.method == 'POST':
        li = LoginInfo(request.POST)
        if li.is_valid():
            userid = li.cleaned_data['userid']
            password = li.cleaned_data['password']
            identity = li.cleaned_data['identity']
            if identity == 'student':
                student = get_object_or_404(Student, id=userid)
                if student.password == password:
                    request.session['id'] = userid
                    request.session['name'] = student.sname
                    return HttpResponseRedirect(reverse('app:student'))
                else:
                    return HttpResponseRedirect(reverse('app:login'))
            else:
                admin = get_object_or_404(Admin, id=userid)
                if admin.password == password:
                    request.session['id'] = userid
                    request.session['name'] = admin.aname
                    return HttpResponseRedirect(reverse('app:admin_index'))
                else:
                    return HttpResponseRedirect(reverse('app:login'))
        else:
            return HttpResponse("li is not valid")
    else:
        default_login = {'userid': 1, 'password': 'password', 'identity': 'student'}
        li = LoginInfo(default_login)
        return render(request, 'app/login.html', {'loginInfo': li})

def logout(request):
    try:
        del request.session['id']
        del request.session['name']
    except KeyError:
        return HttpResponse("KeyError")
    return HttpResponseRedirect(reverse('app:login'))

class BookInfo(forms.Form):
    bname = forms.CharField(max_length=30, label='书名：', widget=forms.TextInput(attrs={
        'class': 'text'
    }))
    bcount = forms.IntegerField(label='数量：', widget=forms.NumberInput(attrs={
        'class': 'text'
    }))
    bposition = forms.CharField(max_length=50, label='位置：', widget=forms.TextInput(attrs={
        'class': 'text'
    }))
    bintroduction = forms.CharField(label='简介：', widget=forms.Textarea(attrs={
        'class': 'text',
        'rows': 10,
        'style': 'resize: none'
    }))
    btype_list = []
    for type in list(Type.objects.all()):
        btype_list.append((type.id, type.tname))
    btype = forms.ChoiceField(choices=btype_list, label='类型：')

def admin_index(request):
    if request.method == 'POST':
        bookInfo = BookInfo(request.POST)
        if bookInfo.is_valid():
            bname = bookInfo.cleaned_data['bname']
            bcount = bookInfo.cleaned_data['bcount']
            bposition = bookInfo.cleaned_data['bposition']
            btype = bookInfo.cleaned_data['btype']
            bintroduction = bookInfo.cleaned_data['bintroduction']
            Book.objects.create(bname=bname,bcount=bcount,bposition=bposition,btype=Type.objects.get(id=btype),bintroduction=bintroduction)
            return HttpResponseRedirect(reverse('app:admin_index'))
        else:
            return HttpResponse("bookInfo is not valid")
    else:
        bookInfo = BookInfo()
        book_list = Book.objects.all()
        borrow = Borrow.objects.all()
        return render(request, 'app/admin_index.html', {'bookInfo': bookInfo, 'book_list': book_list, 'borrow': borrow})

def admin_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'app/admin_detail.html', {'book': book})

def delete(request, book_id):
    Book.objects.get(id=book_id).delete()
    return HttpResponseRedirect(reverse('app:admin_index'))

class SignupInfo(forms.Form):
    sname = forms.CharField(
        max_length=10, label='Name',
        widget=forms.TextInput(attrs={
            'class': 'text',
            'autofocus': 'true',
            'title': '请输入用户名'
        })
    )
    sage = forms.IntegerField(
        widget=forms.TextInput(attrs={
            'class': 'text',
            'pattern': '^[\d]*$',
            'title': '年龄必须为数字'
        })
    )
    password = forms.CharField(
        label='Passwd',
        widget=forms.TextInput(attrs={
            'class': 'text',
            'pattern': '^(?=.{8,}).*$',
            'title': '密码必须大于等于8位'
        })
    )

    dept_list = []
    for dept in Department.objects.all():
        dept_list.append((dept.id, dept.dname))

    dept = forms.ChoiceField(choices=dept_list)

def signup(request):
    if request.method == 'POST':
        # si signupinfo
        si = SignupInfo(request.POST)
        if si.is_valid():
            print(request)
            sname = si.cleaned_data['sname']
            sage = si.cleaned_data['sage']
            password = si.cleaned_data['password']
            sdept = si.cleaned_data['dept']
            student = Student.objects.get_or_create(
                sname = sname,
                sage = sage,
                password = password,
                sdepartment = Department.objects.get(id=sdept)
            )
            return HttpResponse("your id is "+str(student[0].id))
        else:
            return HttpResponse("si is not valid")
    else:
        si = SignupInfo()
        return render(request, 'app/signup.html', {'signupInfo': si})