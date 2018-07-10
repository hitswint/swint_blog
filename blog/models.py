# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from markdownx.models import MarkdownxField


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
    0: u'Normal',
    1: u'Draft',
    2: u'Deleted',
}


# * Category
class Category(models.Model):
    name = models.CharField(
        default=u'unknown', unique=True, max_length=40, verbose_name=u'name')
    parent = models.ForeignKey(
        'self', default=None, blank=True, null=True, verbose_name=u'parent')
    rank = models.IntegerField(default=0, verbose_name=u'rank')
    status = models.IntegerField(
        default=0, choices=STATUS.items(), verbose_name=u'status')

    create_time = models.DateTimeField(u'create_time', auto_now_add=True)

    class Meta:
        verbose_name_plural = verbose_name = u'category'
        ordering = ['rank', '-create_time']
        app_label = string_with_title('blog', u"Blog Management")

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
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, default=1, verbose_name=u'author')
    # category = models.ForeignKey(Category, verbose_name=u'分类')
    # 引用外键Category，Category定义需在Article前面。
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_DEFAULT,
        to_field='name',
        # null=True,
        default=u'unknown',
        verbose_name=u'category')
    title = models.CharField(max_length=100, verbose_name=u'title')
    subtitle = models.CharField(max_length=100, verbose_name=u'subtitle')
    img = models.CharField(max_length=200, default='/static/img/default.jpg')
    tags = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name=u'tag',
        help_text=u'seperated by comma')
    content = models.TextField(verbose_name=u'content')
    # content = MarkdownxField()
    view_times = models.IntegerField(default=0)
    zan_times = models.IntegerField(default=0)

    is_top = models.BooleanField(default=False, verbose_name=u'is_top')
    rank = models.IntegerField(default=0, verbose_name=u'rank')
    status = models.IntegerField(
        default=0, choices=STATUS.items(), verbose_name='status')
    pub_time = models.DateTimeField(default=False, verbose_name=u'pub_time')
    create_time = models.DateTimeField(u'create_time', auto_now_add=True)
    update_time = models.DateTimeField(u'update_time', auto_now=True)

    def get_tags(self):
        # 删除字符串中的空格并用逗号分割。
        tags_without_space = ''.join([x for x in self.tags if x != " "])
        tags_list = self.tags.split(',')
        while '' in tags_list:
            tags_list.remove('')

        return tags_list

    class Meta:
        verbose_name_plural = verbose_name = u'article'
        ordering = ['rank', '-is_top', '-pub_time', '-create_time']
        app_label = string_with_title('blog', u"Blog Management")

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
