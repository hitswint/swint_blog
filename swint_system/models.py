# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings

# Create your models here.

IS_READ = {0: u'unread', 1: u'read'}


class Notification(models.Model):
    title = models.CharField(max_length=100, verbose_name=u'title')
    text = models.TextField(verbose_name=u'text')
    url = models.CharField(
        max_length=200, verbose_name=u'url', null=True, blank=True)
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        default=None,
        blank=True,
        null=True,
        related_name='from_user_notification_set',
        verbose_name=u'from_user')
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='to_user_notification_set',
        verbose_name=u'to_user')
    type = models.CharField(
        max_length=20, verbose_name=u'type', null=True, blank=True)

    is_read = models.IntegerField(
        default=0, choices=IS_READ.items(), verbose_name=u'is_read')

    create_time = models.DateTimeField(u'create_time', auto_now_add=True)
    update_time = models.DateTimeField(u'update_time', auto_now=True)

    class Meta:
        verbose_name_plural = verbose_name = u'Notification'
        ordering = ['-create_time']


class Link(models.Model):
    title = models.CharField(max_length=100, verbose_name=u'title')
    url = models.CharField(
        max_length=200, verbose_name=u'url', null=True, blank=True)
    type = models.CharField(
        max_length=20, verbose_name=u'type', null=True, blank=True)

    create_time = models.DateTimeField(u'create_time', auto_now_add=True)
    update_time = models.DateTimeField(u'update_time', auto_now=True)

    class Meta:
        verbose_name_plural = verbose_name = u'Link'
        ordering = ['-create_time']
