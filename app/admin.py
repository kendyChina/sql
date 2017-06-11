from django.contrib import admin

# Register your models here.

from .models import Department, Student, Type, Book, Borrow, Admin

admin.site.register(Department)
admin.site.register(Student)
admin.site.register(Type)
admin.site.register(Book)
admin.site.register(Borrow)
admin.site.register(Admin)