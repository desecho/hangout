# -*- coding: utf8 -*-
from hangout.models import UserMeeting


def disable_availability(user_data):
    def update_meeting_data(user):
        def user_in_meeting():
            user_meetings = UserMeeting.objects.filter(user_data__user=user)
            if user_meetings.exists():
                return user_meetings[0]

        def close_meeting_if_necessary(meeting):
            if UserMeeting.objects.filter(meeting=meeting).count() < 2:
                meeting.active = False
                meeting.save()

        user_in_meeting = user_in_meeting()
        if user_in_meeting:
            close_meeting_if_necessary(user_in_meeting.meeting)
            user_in_meeting.delete()

    update_meeting_data(user_data.user)
    user_data.location = ''
    user_data.availability = False
    user_data.timer_disable_time = None
    user_data.save()
