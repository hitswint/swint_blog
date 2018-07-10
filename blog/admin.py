# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
from blog.models import Article, Category, Profile
from markdownx.widgets import AdminMarkdownxWidget


# * CategoryAdmin
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('name', )
    list_filter = ('status', 'create_time')
    list_display = ('name', 'parent', 'rank', 'status')
    fields = ('name', 'parent', 'rank', 'status')


# * ArticleAdmin
class ArticleAdmin(admin.ModelAdmin):
    search_fields = ('title', 'summary', 'content')
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
    formfield_overrides = {
        models.TextField: {
            'widget': AdminMarkdownxWidget
        },
    }


# * ProfileAdmin
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Profile, ProfileAdmin)
