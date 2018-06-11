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

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index-view'),
    url(r'^article/(?P<id>\w+).html$',
        ArticleView.as_view(),
        name='article-detail-view'),
    url(r'^all/$', AllView.as_view(), name='all-view'),
    url(r'^search/$', SearchView.as_view(), name='search-view'),
    url(r'^about/$', about, name='about'),
    url(r'^tag/(?P<tag>\w+)/$', TagView.as_view(), name='tag-detail-view'),
    url(r'^category/(?P<category>\w+)/$',
        CategoryView.as_view(),
        name='category-detail-view'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^logout-then-login/$',
        LogoutView.as_view(next_page=settings.LOGIN_URL),
        name='logout_then_login'),
    # change password
    url(r'^password-change/$',
        PasswordChangeView.as_view(),
        name='password_change'),
    url(r'^password-change/done/$',
        PasswordChangeDoneView.as_view(),
        name='password_change_done'),
    # reset password
    ## restore password urls
    url(r'^password-reset/$',
        PasswordResetView.as_view(),
        name='password_reset'),
    url(r'^password-reset/done/$',
        PasswordResetDoneView.as_view(),
        name='password_reset_done'),
    url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',
        PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'),
    url(r'^password-reset/complete/$',
        PasswordResetCompleteView.as_view(),
        name='password_reset_complete'),
    url(r'^register/$', register, name='register'),
    url(r'^edit/$', edit, name='edit'),
    url(r'^dashboard$', dashboard, name='dashboard'),
]
