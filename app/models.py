from django.db import models
import datetime
from django.utils import timezone
# Create your models here.

class Department(models.Model):
    dname = models.CharField(max_length=10) #专业名

    def __str__(self):
        return self.dname

class Student(models.Model):
    sname = models.CharField(max_length=10) #姓名
    sage = models.IntegerField() #年龄
    sdepartment = models.ForeignKey(Department, on_delete=models.CASCADE) #专业
    password = models.CharField(max_length=10)

    def __str__(self):
        return self.sname

class Type(models.Model): #书本类型
    tname = models.CharField(max_length=30) #种类名

    def __str__(self):
        return self.tname

class Book(models.Model):
    bname = models.CharField(max_length=30) #书名
    bcount = models.IntegerField() #数量
    bposition = models.CharField(max_length=50) #位置
    btype = models.ForeignKey(Type) #类型
    bintroduction = models.TextField(blank=True) # 简介

    def __str__(self):
        return self.bname

class Borrow(models.Model):
    student = models.ForeignKey(Student)
    book = models.ForeignKey(Book)
    borrow_time = models.DateField(
        '借书日期',
        default = timezone.now
    )
    should_return = models.DateField(
        '应还日期',
        default = timezone.now() + datetime.timedelta(days=30)
    )

    def __str__(self):
        return self.student.sname+','+self.book.bname+','+self.borrow_time.strftime("%Y-%m-%d")
    def was_overdue(self):
        return timezone.now() > self.should_return

class Admin(models.Model):
    aname = models.CharField(max_length=10)
    password = models.CharField(max_length=10)

    def __str__(self):
        return self.aname