from django.conf.urls import url
from django.views.generic import TemplateView
from django.contrib.auth.views import login
from django.contrib.auth.views import logout
from django.contrib.auth.views import logout_then_login
from django.contrib.auth.views import password_change
from django.contrib.auth.views import password_change_done
from django.contrib.auth.views import password_reset
from django.contrib.auth.views import password_reset_done
from django.contrib.auth.views import password_reset_confirm
from django.contrib.auth.views import password_reset_complete
from blog.views import *

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index-view'),
    url(r'^article/(?P<slug>\w+).html$',
        ArticleView.as_view(),
        name='article-detail-view'),
    url(r'^all/$', AllView.as_view(), name='all-view'),
    url(r'^search/$', SearchView.as_view()),
    url(r'^tag/(?P<tag>\w+)/$', TagView.as_view(), name='tag-detail-view'),
    url(r'^category/(?P<category>\w+)/$',
        CategoryView.as_view(),
        name='category-detail-view'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^logout-then-login/$', logout_then_login, name='logout_then_login'),
    # change password
    url(r'^password-change/$', password_change, name='password_change'),
    url(r'^password-change/done/$',
        password_change_done,
        name='password_change_done'),
    # reset password
    ## restore password urls
    url(r'^password-reset/$', password_reset, name='password_reset'),
    url(r'^password-reset/done/$',
        password_reset_done,
        name='password_reset_done'),
    url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',
        password_reset_confirm,
        name='password_reset_confirm'),
    url(r'^password-reset/complete/$',
        password_reset_complete,
        name='password_reset_complete'),
    url(r'^register/$', register, name='register'),
]
