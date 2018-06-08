# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings


# * string_with_title
class string_with_title(str):
    """ 用来修改admin中显示的app名称,因为admin app 名称是用 str.title()显示的,
    所以修改str类的title方法就可以实现.
    """

    def __new__(cls, value, title):
        instance = str.__new__(cls, value)
        instance._title = title
        return instance

    def title(self):
        return self._title

    __copy__ = lambda self: self
    __deepcopy__ = lambda self, memodict: self


# Create your models here.
STATUS = {
    0: u'正常',
    1: u'草稿',
    2: u'删除',
}


# * Category
class Category(models.Model):
    name = models.CharField(
        default=u'未分类', unique=True, max_length=40, verbose_name=u'名称')
    parent = models.ForeignKey(
        'self', default=None, blank=True, null=True, verbose_name=u'上级分类')
    rank = models.IntegerField(default=0, verbose_name=u'排序')
    status = models.IntegerField(
        default=0, choices=STATUS.items(), verbose_name=u'状态')

    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)

    class Meta:
        verbose_name_plural = verbose_name = u'分类'
        ordering = ['rank', '-create_time']
        app_label = string_with_title('blog', u"博客管理")

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('category-detail-view', args=(self.name, ))

    def __unicode__(self):
        if self.parent:
            return '%s-->%s' % (self.parent, self.name)
        else:
            return '%s' % (self.name)

    __str__ = __unicode__


# * Article
class Article(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'作者')
    # category = models.ForeignKey(Category, verbose_name=u'分类')
    # 引用外键Category，Category定义需在Article前面。
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_DEFAULT,
        to_field='name',
        # null=True,
        default=u'未分类',
        verbose_name=u'类别')
    title = models.CharField(max_length=100, verbose_name=u'标题')
    subtitle = models.CharField(max_length=100, verbose_name=u'子标题')
    img = models.CharField(
        max_length=200, default='/static/img/article/default.jpg')
    tags = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name=u'标签',
        help_text=u'逗号分隔')
    summary = models.TextField(verbose_name=u'摘要')
    content = models.TextField(verbose_name=u'正文')
    view_times = models.IntegerField(default=0)
    zan_times = models.IntegerField(default=0)

    is_top = models.BooleanField(default=False, verbose_name=u'置顶')
    rank = models.IntegerField(default=0, verbose_name=u'排序')
    status = models.IntegerField(
        default=0, choices=STATUS.items(), verbose_name='状态')
    pub_time = models.DateTimeField(default=False, verbose_name=u'发布时间')
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True)

    def get_tags(self):
        tags_list = self.tags.split(',')
        while '' in tags_list:
            tags_list.remove('')

        return tags_list

    class Meta:
        verbose_name_plural = verbose_name = u'文章'
        ordering = ['rank', '-is_top', '-pub_time', '-create_time']
        app_label = string_with_title('blog', u"博客管理")

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('article-detail-view', args=(self.id, ))

    def __unicode__(self):
        return self.title

    __str__ = __unicode__


def user_directory_path(instance, filename):
    #pdb.set_trace()
    return 'users/{0}/{1}'.format(instance.user.username, filename)


# * Profile
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    date_of_birth = models.DateField(blank=True, null=True)
    # photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)
    photo = models.ImageField(upload_to=user_directory_path, blank=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)
