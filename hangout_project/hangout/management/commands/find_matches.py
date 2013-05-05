from django.core.management.base import BaseCommand
from hangout.models import UserData, Meeting, UserMeeting, Visibility
import random
import googl
from hangout import littlesms
from django.conf import settings
from django.contrib.sites.models import Site


class Command(BaseCommand):
    help = 'Finds matches'

    def handle(self, *args, **options):
        sms = littlesms.Api(settings.LITTLESMS_API_USER, settings.LITTLESMS_API_KEY)

        def add_users_to_meeting(users_data, meeting):
            for user_data in users_data:
                UserMeeting(meeting=meeting, user_data=user_data).save()

        def get_random_user_data(users_data):
            id = random.randrange(0, users_data.count())
            return users_data[id]

        def send_sms_messages(users_data, meeting, organizer=None, user_data_all=None):
            def send_sms(message, to):
                if settings.SEND_SMS:
                    sms.send(message, to, sender='Hangout')
                print(message, to)

            def get_users(users_data):
                return ', '.join([x.user.username for x in users_data])

            def get_phone_of_user_at_meeting():
                users_new = users_data.values_list('pk')
                users_new = [x[0] for x in users_new]
                users_meeting = user_data_all.exclude(pk__in=users_new)
                return get_random_user_data(users_meeting).phone

            if user_data_all:
                users = get_users(user_data_all)
            else:
                users = get_users(users_data)
            message = 'Uchastniki - %s. Podrobnee - %s' % (users, meeting.url)
            if user_data_all:
                message_meeting = 'Novye Uchastniki! ' + message
                message = 'Vstrecha uzhe idet! ' + message
                send_sms(message_meeting, get_phone_of_user_at_meeting())
            if organizer:
                message_organizer = 'Vy organizator! ' + message
                users_data = users_data.exclude(pk=organizer.pk)
                send_sms(message_organizer, organizer.phone)
            send_sms(message, [x.phone for x in users_data])

        def start_meeting(users_data):
            def create_meeting():
                def shorten_url(url):
                    api = googl.Googl(settings.GOOGLE_API_KEY)
                    link = api.shorten(url)
                    return link['id']
                meeting = Meeting()
                meeting.save()
                meeting.url = shorten_url('%s/meeting/%d' % (Site.objects.get_current().domain, meeting.pk))
                meeting.save()
                return meeting

            meeting = create_meeting()
            add_users_to_meeting(users_data, meeting)
            send_sms_messages(users_data, meeting, get_random_user_data(users_data))

        def get_users_not_in_meeting(users_data):
            users_meeting = UserMeeting.objects.filter(meeting__active=True)
            if users_meeting:
                users_meeting = users_meeting.values_list('user_data')
                users_meeting = [x[0] for x in users_meeting]
                return users_data.exclude(pk__in=users_meeting)

        def get_meeting():
            meeting = Meeting.objects.filter(active=True)
            if meeting.exists():
                return meeting

        def find_matches_3(users_data):
            if users_data.count() > 2:
                users_meeting_new = get_users_not_in_meeting(users_data)
                if users_meeting_new:
                    meeting = get_meeting()
                    add_users_to_meeting(users_meeting_new, meeting)
                    send_sms_messages(users_meeting_new, meeting, None, users_data)
                else:
                    start_meeting(users_data)

        def find_matches_2(users_data):
            def users_can_see_each_other():
                user1 = users_data[0].user
                user2 = users_data[1].user
                user1_visible_to_all = users_data[0].visible_to_all
                user2_visible_to_all = users_data[1].visible_to_all
                return check_if_user_is_visible(user1, user2, user1_visible_to_all) and check_if_user_is_visible(user2, user1, user2_visible_to_all)

            def check_if_user_is_visible(user, friend, visible_to_all):
                if not visible_to_all:
                    return Visibility.objects.get(user=user, friend=friend).visible_updated
                return True

            if not get_meeting():
                users_data = users_data.filter(one_on_one=True)
                if users_data.count() == 2:
                    if users_can_see_each_other():
                        start_meeting(users_data)

        users_data = UserData.objects.filter(availability=True)
        find_matches_3(users_data)
        find_matches_2(users_data)