# -*- coding: utf8 -*-
from django.db import models
from django.contrib.auth.models import User


class UserData(models.Model):
    user = models.ForeignKey(User, verbose_name='пользователь')
    availability = models.BooleanField('доступность')
    one_on_one = models.BooleanField('1 - 1')
    location = models.CharField('местонахождение', max_length=255, null=True,
                                blank=True)
    message = models.CharField('сообщение', max_length=255, null=True,
                               blank=True)
    phone = models.BigIntegerField('телефон')
    timer_disable_time = models.DateTimeField(
        'время отключения доступности по таймеру', null=True, blank=True)
    sleep_disable_time = models.TimeField('время автоотключения доступности')
    visible_to_all = models.BooleanField('видим всем', default=True)

    class Meta:
        verbose_name = 'данные пользователя'
        verbose_name_plural = 'данные пользователей'

    def __unicode__(self):
        return self.user.username


class Visibility(models.Model):
    user = models.ForeignKey(User, related_name='user',
                             verbose_name='пользователь')
    friend = models.ForeignKey(User, related_name='friend', verbose_name='друг')
    visible = models.BooleanField('видимость', default=True)
    visible_updated = models.BooleanField('видимость_обновленная', default=True)

    class Meta:
        verbose_name = 'видимость'
        verbose_name_plural = 'видимости'

    def __unicode__(self):
        return self.user.username + ' - ' + self.friend.username


class Group(models.Model):
    name = models.CharField('название', max_length=255)

    class Meta:
        verbose_name = 'группа'
        verbose_name_plural = 'группы'

    def __unicode__(self):
        return self.name


class UserGroup(models.Model):
    user = models.ForeignKey(User, verbose_name='пользователь')
    group = models.ForeignKey(Group, verbose_name='группа')

    class Meta:
        verbose_name = 'пользователь-группа'
        verbose_name_plural = 'пользователи-группы'

    def __unicode__(self):
        return self.user.username + ' - ' + self.group.name


class Meeting(models.Model):
    active = models.BooleanField('активная', default=True)
    url = models.URLField(max_length=20)

    class Meta:
        verbose_name = 'встреча'
        verbose_name_plural = 'встречи'

    def __unicode__(self):
        return str(self.id) + ' - ' + str(self.active)


class UserMeeting(models.Model):
    meeting = models.ForeignKey(Meeting, verbose_name='встреча')
    user_data = models.ForeignKey(UserData, verbose_name='данные пользователя')

    class Meta:
        verbose_name = 'пользователь-встреча'
        verbose_name_plural = 'пользователи-встречи'

    def __unicode__(self):
        return str(self.meeting.id) + ' - ' + self.user_data.user.username
