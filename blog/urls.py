from django.conf.urls import url
from django.conf import settings
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
# from django.contrib.auth.views import logout_then_login
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.views import PasswordChangeDoneView
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.views import PasswordResetDoneView
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.views import PasswordResetCompleteView
from blog.views import *
from django.urls import reverse, path, re_path

urlpatterns = [
    re_path(r'^$', IndexView.as_view(), name='index-view'),
    re_path(r'^article/(?P<id>\w+).html$',
        ArticleView.as_view(),
        name='article-detail-view'),
    re_path(r'^all/$', AllView.as_view(), name='all-view'),
    re_path(r'^search/$', SearchView.as_view(), name='search-view'),
    re_path(r'^about/$', about, name='about'),
    re_path(r'^tag/(?P<tag>\w+)/$', TagView.as_view(), name='tag-detail-view'),
    re_path(r'^category/(?P<category>\w+)/$',
        CategoryView.as_view(),
        name='category-detail-view'),
    re_path(r'^login/$', LoginView.as_view(), name='login'),
    re_path(r'^logout/$', LogoutView.as_view(), name='logout'),
    re_path(r'^logout-then-login/$',
        LogoutView.as_view(next_page=settings.LOGIN_URL),
        name='logout_then_login'),
    # change password
    re_path(r'^password-change/$',
        PasswordChangeView.as_view(),
        name='password_change'),
    re_path(r'^password-change/done/$',
        PasswordChangeDoneView.as_view(),
        name='password_change_done'),
    # reset password
    ## restore password urls
    re_path(r'^password-reset/$',
        PasswordResetView.as_view(),
        name='password_reset'),
    re_path(r'^password-reset/done/$',
        PasswordResetDoneView.as_view(),
        name='password_reset_done'),
    re_path(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',
        PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'),
    re_path(r'^password-reset/complete/$',
        PasswordResetCompleteView.as_view(),
        name='password_reset_complete'),
    re_path(r'^register/$', register, name='register'),
    re_path(r'^edit/$', edit, name='edit'),
    re_path(r'^dashboard$', dashboard, name='dashboard'),
]
