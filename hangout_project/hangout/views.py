# -*- coding: utf8 -*-
import json
from django.shortcuts import redirect
from hangout.models import UserData, Visibility, Meeting, UserMeeting
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from annoying.decorators import ajax_request, render_to
from django.http import HttpResponse
from datetime import datetime
from dateutil.relativedelta import relativedelta

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
    users = Visibility.objects.filter(user=request.user).values_list('friend', 'friend__username', 'visible', 'visible_updated')
    users = [{'id': x[0], 'name': x[1], 'visible': x[2], 'visible_updated': x[3]} for x in users]
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
    def remove_location_if_necessary(data):
        if not data.availability:
            data.location = ''
        return data

    def update_meeting_data():
        if not value:
            if UserMeeting.objects.filter(user_data__user=request.user).exists():
                user_meeting = UserMeeting.objects.get(user_data__user=request.user)
                meeting = user_meeting.meeting
                user_meeting.delete()
                if UserMeeting.objects.filter(meeting=meeting).count() < 2:
                    meeting.active = False
                    meeting.save()

    if request.is_ajax() and request.method == 'POST':
        POST = request.POST
        data = UserData.objects.get(user=request.user)
        if 'message' in POST:
            data.message = POST['message']
        if 'one_on_one' in POST:
            data.one_on_one = int(POST['one_on_one'])
        if 'availability' in POST:
            value = int(POST['availability'])
            data.availability = value
            update_meeting_data()
            data = remove_location_if_necessary(data)
        if 'visible_to_all' in POST:
            data.visible_to_all = int(POST['visible_to_all'])
        if 'location' in POST:
            location = json.loads(POST['location'])
            location = [str(x) for x in location]
            data.location = ','.join(location)
        data.save()
        return HttpResponse()

def change_visibility(request):
    if request.is_ajax() and request.method == 'POST':
        POST = request.POST
        if 'id' in POST and 'value' in POST:
            value = int(POST['value'])
            visibility = Visibility.objects.get(user=request.user, friend=int(POST['id']))
            if visibility.visible_updated != value:
                visibility.visible_updated = value
                visibility.save()
        return HttpResponse()
