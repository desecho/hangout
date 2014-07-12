# -*- coding: utf8 -*-
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse
from annoying.decorators import render_to

from .models import UserData, Visibility, Meeting, UserMeeting
from .general import disable_availability


def logout_view(request):
    logout(request)
    return redirect('/login/')


@render_to('help.html')
@login_required
def help(request):
    return {}


@render_to('index.html')
@login_required
def home(request):
    data = UserData.objects.get(user=request.user)
    return {'data': data, 'google_api_key': settings.GOOGLE_MAPS_API_KEY}


@render_to('visibility.html')
@login_required
def visibility(request):
    users = Visibility.objects.filter(user=request.user) \
                              .values_list('friend', 'friend__username',
                                           'visible', 'visible_updated')
    users = [{'id': x[0], 'name': x[1], 'visible': x[2],
              'visible_updated': x[3]} for x in users]
    data = UserData.objects.get(user=request.user)
    return {'users': users, 'data': data}


@render_to('meeting.html')
@login_required
def meeting(request, id):
    output = {'google_api_key': settings.GOOGLE_MAPS_API_KEY}
    meeting = Meeting.objects.get(pk=id)
    if meeting.active:
        users_meeting = UserMeeting.objects.filter(meeting=meeting)
        users_data = [x.user_data for x in users_meeting]
        output['users_data'] = users_data
    else:
        message = 'Встреча окончена.'
        output['message'] = message
    return output


def update_data(request):
    if request.is_ajax() and request.method == 'POST':
        POST = request.POST
        data = UserData.objects.get(user=request.user)
        if 'message' in POST:
            data.message = POST['message']
        if 'one_on_one' in POST:
            data.one_on_one = int(POST['one_on_one'])
        if 'visible_to_all' in POST:
            data.visible_to_all = int(POST['visible_to_all'])
        if 'location' in POST:
            location = json.loads(POST['location'])
            location = [str(x) for x in location]
            data.location = ','.join(location)
        if 'sleep_time' in POST:
            data.sleep_disable_time = datetime.strptime(POST['sleep_time'],
                                                        settings.TIME_FORMAT)
        if 'timer' in POST:
            timer = datetime.strptime(POST['timer'], settings.TIME_FORMAT)
            data.timer_disable_time = datetime.now() + relativedelta(
                hours=timer.hour, minutes=timer.minute)
        data.save()
        if 'availability' in POST:
            availability = int(POST['availability'])
            if not availability:
                disable_availability(data)
            else:
                data.availability = True
                data.save()
        return HttpResponse()


def change_visibility(request):
    if request.is_ajax() and request.method == 'POST':
        POST = request.POST
        if 'id' in POST and 'value' in POST:
            value = int(POST['value'])
            visibility = Visibility.objects.get(user=request.user,
                                                friend=int(POST['id']))
            if visibility.visible_updated != value:
                visibility.visible_updated = value
                visibility.save()
        return HttpResponse()
