# -*- coding: utf-8 -*-
from django.contrib import admin
from blog.models import Article, Category, Profile


# * CategoryAdmin
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('name', )
    list_filter = ('status', 'create_time')
    list_display = ('name', 'parent', 'rank', 'status')
    fields = ('name', 'parent', 'rank', 'status')


# * ArticleAdmin
class ArticleAdmin(admin.ModelAdmin):
    search_fields = ('title', 'summary')
    list_filter = ('status', 'category', 'is_top', 'create_time',
                   'update_time', 'is_top')
    list_display = ('title', 'category', 'author', 'status', 'is_top',
                    'update_time')
    fieldsets = ((u'info', {
        'fields': ('title', 'subtitle', 'img', 'category', 'tags', 'author',
                   'is_top', 'rank', 'status')
    }), (u'content', {
        'fields': ('content', )
    }), (u'time', {
        'fields': ('pub_time', )
    }), )


# * ProfileAdmin
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo']


# class NewsAdmin(admin.ModelAdmin):
#     search_fields = ('title', 'summary')
#     list_filter = ('news_from', 'create_time')
#     list_display = ('title', 'news_from', 'url', 'create_time')
#     fields = ('title', 'news_from', 'url', 'summary', 'pub_time')

# class NavAdmin(admin.ModelAdmin):
#     search_fields = ('name',)
#     list_display = ('name', 'url', 'status', 'create_time')
#     list_filter = ('status', 'create_time')
#     fields = ('name', 'url', 'status')

# class ColumnAdmin(admin.ModelAdmin):
#     search_fields = ('name',)
#     list_display = ('name', 'status', 'create_time')
#     list_filter = ('status', 'create_time')
#     fields = ('name', 'status', 'article', 'summary')
#     filter_horizontal = ('article',)

# class CarouselAdmin(admin.ModelAdmin):
#     search_fields = ('title',)
#     list_display = ('title', 'article', 'img', 'create_time')
#     list_filter = ('create_time',)
#     fields = ('title', 'article', 'img', 'summary')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Profile, ProfileAdmin)
# admin.site.register(News, NewsAdmin)
# admin.site.register(Nav, NavAdmin)
# admin.site.register(Column, ColumnAdmin)
# admin.site.register(Carousel, CarouselAdmin)
