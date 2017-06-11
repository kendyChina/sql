from django.conf.urls import url
from . import views

app_name = 'app'
urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^login/$', views.login, name='login'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^logout/$', views.logout, name='logout'),

    url(r'^student/$', views.student, name='student'),
    url(r'^detail/(?P<book_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^borrow/(?P<book_id>[0-9]+)/$', views.borrow, name='borrow'),
    url(r'^return_book/(?P<book_id>[0-9]+)/$', views.return_book, name='return_book'),

    url(r'^admin_index/$', views.admin_index, name='admin_index'),
    url(r'^admin_detail/(?P<book_id>[0-9]+)/$', views.admin_detail, name='admin_detail'),
    url(r'^delete/(?P<book_id>[0-9]+)/$', views.delete, name='delete'),
]
