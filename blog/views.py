# -*- coding: utf-8 -*-
from django import template
from django import forms
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.template import Context, loader
from django.views.generic import View, TemplateView, ListView, DetailView
from django.db.models import Q
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.contrib import auth
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm, UserCreationForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from blog.models import Article, Category, Profile
from blog.forms import UserCreationFormCustomized, UserEditForm, ProfileEditForm
from swint_system.models import Link
from django.conf import settings
import datetime
import time
import json
import logging

# 缓存
# try:
#     cache = caches['memcache']
# except ImportError as e:
#     cache = caches['default']

# logger
logger = logging.getLogger(__name__)


# * BaseMixin
class BaseMixin(object):
    def get_context_data(self, *args, **kwargs):
        context = super(BaseMixin, self).get_context_data(**kwargs)
        try:
            # 网站标题等内容
            context['website_title'] = settings.WEBSITE_TITLE
            context['website_welcome'] = settings.WEBSITE_WELCOME
            # 热门文章
            context['hot_article_list'] = Article.objects.order_by(
                "-view_times")[0:10]
            # 友情链接
            context['links'] = Link.objects.order_by('create_time').all()
            colors = ['primary', 'success', 'info', 'warning', 'danger']
            for index, link in enumerate(context['links']):
                link.color = colors[index % len(colors)]

        except Exception as e:
            logger.error(u'[BaseMixin]加载基本信息出错')

        return context


# * IndexView
class IndexView(BaseMixin, ListView):
    template_name = 'blog/index.html'
    context_object_name = 'article_list'
    paginate_by = settings.PAGE_NUM  # 分页--每页的数目

    def get_context_data(self, **kwargs):
        kwargs['bg_img'] = 'home-bg.jpg'
        kwargs['heading'] = 'Swint \'s blog'
        kwargs['subheading'] = settings.WEBSITE_WELCOME
        return super(IndexView, self).get_context_data(**kwargs)

    def get_queryset(self):
        article_list = Article.objects.filter(status=0)
        return article_list


# * ArticleView
class ArticleView(BaseMixin, DetailView):
    queryset = Article.objects.filter(Q(status=0) | Q(status=1))
    template_name = 'blog/article.html'
    context_object_name = 'article'
    # 从url中获得id值为slug_url_kwarg，并在queryset中使用slug_field过滤。
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def get(self, request, *args, **kwargs):
        # 统计文章的访问访问次数
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']

        self.cur_user_ip = ip

        article_id = self.kwargs.get('id')
        # 获取15*60s时间内访问过这篇文章的所有ip
        visited_ips = cache.get(article_id, [])

        # 如果ip不存在就把文章的浏览次数+1
        if ip not in visited_ips:
            try:
                article = self.queryset.get(id=article_id)
            except Article.DoesNotExist:
                logger.error(u'[ArticleView]访问不存在的文章:[%s]' % article_id)
                raise Http404
            else:
                article.view_times += 1
                article.save()
                visited_ips.append(ip)

            # 更新缓存
            cache.set(article_id, visited_ips, 15 * 60)

        return super(ArticleView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['bg_img'] = 'post-bg.jpg'
        return super(ArticleView, self).get_context_data(**kwargs)


# * AllView
class AllView(BaseMixin, ListView):
    template_name = 'blog/all.html'
    context_object_name = 'article_list'

    def get_context_data(self, **kwargs):
        kwargs['category_list'] = Category.objects.all()
        kwargs['PAGE_NUM'] = settings.PAGE_NUM
        return super(AllView, self).get_context_data(**kwargs)

    def get_queryset(self):
        article_list = Article.objects.filter(
            status=0).order_by("-pub_time")[0:settings.PAGE_NUM]
        return article_list

    def post(self, request, *args, **kwargs):
        val = self.request.POST.get("val", "")
        sort = self.request.POST.get("sort", "time")
        start = self.request.POST.get("start", 0)
        end = self.request.POST.get("end", settings.PAGE_NUM)

        start = int(start)
        end = int(end)

        if sort == "time":
            sort = "-pub_time"
        elif sort == "recommend":
            sort = "-view_times"
        else:
            sort = "-pub_time"

        if val == "all":
            article_list = \
                Article.objects.filter(status=0).order_by(sort)[start:end+1]
        else:
            try:
                article_list = Category.objects.get(
                    name=val).article_set.filter(
                        status=0).order_by(sort)[start:end + 1]
            except Category.DoesNotExist:
                logger.error(u'[AllView]此分类不存在:[%s]' % val)
                raise PermissionDenied

        isend = len(article_list) != (end - start + 1)

        article_list = article_list[0:end - start]

        html = ""
        for article in article_list:
            html += template.loader.get_template(
                'blog/include/all_post.html').render({
                    'post': article
                })

        mydict = {"html": html, "isend": isend}
        return HttpResponse(
            json.dumps(mydict), content_type="application/json")


# * about
def about(request):
    return render(request, 'blog/about.html', {'bg_img': "about-bg.jpg"})


# * SearchView
class SearchView(BaseMixin, ListView):
    template_name = 'blog/search.html'
    context_object_name = 'article_list'
    paginate_by = settings.PAGE_NUM

    def get_context_data(self, **kwargs):
        kwargs['s'] = self.request.GET.get('s', '')
        return super(SearchView, self).get_context_data(**kwargs)

    def get_queryset(self):
        # 获取搜索的关键字
        s = self.request.GET.get('s', '')
        # 在文章的标题,summary和tags中搜索关键字
        article_list = Article.objects.only(
            'title', 'subtitle', 'tags').filter(
                Q(title__icontains=s) | Q(subtitle__icontains=s) |
                Q(tags__icontains=s),
                status=0)
        return article_list


# * TagView
class TagView(BaseMixin, ListView):
    template_name = 'blog/tag.html'
    context_object_name = 'article_list'
    paginate_by = settings.PAGE_NUM

    def get_queryset(self):
        tag = self.kwargs.get('tag', '')
        article_list = \
            Article.objects.only('tags').filter(tags__icontains=tag, status=0)

        return article_list

    def get_context_data(self, **kwargs):
        kwargs['tag'] = self.kwargs.get('tag', '')
        return super(TagView, self).get_context_data(**kwargs)


# * CategoryView
class CategoryView(BaseMixin, ListView):
    template_name = 'blog/category.html'
    context_object_name = 'article_list'
    paginate_by = settings.PAGE_NUM

    def get_queryset(self):
        category = self.kwargs.get('category', '')
        try:
            article_list = \
                Category.objects.get(name=category).article_set.all()
        except Category.DoesNotExist:
            logger.error(u'[CategoryView]此分类不存在:[%s]' % category)
            raise Http404

        return article_list

    def get_context_data(self, **kwargs):
        kwargs['category'] = self.kwargs.get('category', '')
        return super(CategoryView, self).get_context_data(**kwargs)


# * register
def register(request):
    if request.method == 'POST':
        user_form = UserCreationFormCustomized(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password1'])
            # Save the User object
            new_user.save()
            profile = Profile.objects.create(user=new_user)
            return render(request, 'registration/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserCreationFormCustomized()
    return render(request, 'registration/register.html',
                  {'user_form': user_form})


# * edit
@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return dashboard(request)
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'registration/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})


# * dashboard
@login_required
def dashboard(request):
    return render(request, 'registration/dashboard.html')
