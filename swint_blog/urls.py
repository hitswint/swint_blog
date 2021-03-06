from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import GenericSitemap, Sitemap
from django.urls import reverse, path, re_path
from django.views.static import serve

from django.contrib import admin

from blog.models import Article, Category


class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = 'daily'

    def items(self):
        return ['index-view', 'news-view']

    def location(self, item):
        return reverse(item)


sitemaps = {
    'article-is-top':
    GenericSitemap(
        {
            'queryset': Article.objects.filter(status=0, is_top=True).all(),
            'date_field': 'pub_time'
        },
        priority=1.0,
        changefreq='daily'),
    'article-is-not-top':
    GenericSitemap(
        {
            'queryset': Article.objects.filter(status=0).all(),
            'date_field': 'pub_time'
        },
        priority=0.8,
        changefreq='daily'),
    'category':
    GenericSitemap(
        {
            'queryset': Category.objects.all()
        }, priority=0.9, changefreq='daily'),
    'static':
    StaticViewSitemap
}

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'', include('blog.urls')),
    re_path(r'^comments/', include('django_comments.urls')),
    re_path(r'^avatar/', include('initial_avatars.urls')),
    re_path(r'^summernote/', include('django_summernote.urls')),
    re_path(r'^markdownx/', include('markdownx.urls')),
    re_path(r'^sitemap\.xml$',
        sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap')
]

# DEBUG = True时，将/media下文件当作静态文件处理。
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Debug = False时，静态文件不会自动加载，而是交给apache/nginx来处理。
# 设置在非调试模式下同样加载静态文件。
if settings.DEBUG is False:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
