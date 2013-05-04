from django.core.management.base import BaseCommand
from hangout.models import UserData, Meeting, UserMeeting
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
                sms.send(message, to, sender='Hangout')
                #sms.send(message, to)
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

        def find_matches_3():
            users_data = UserData.objects.filter(availability=True)
            if users_data.count() >= 3:
                users_meeting = UserMeeting.objects.filter(meeting__active=True)
                if users_meeting:
                    meeting = users_meeting[0].meeting
                    users_meeting = users_meeting.values_list('user_data')
                    users_meeting = [x[0] for x in users_meeting]
                    users_meeting_new = users_data.exclude(pk__in=users_meeting)
                    if users_meeting_new:
                        add_users_to_meeting(users_meeting_new, meeting)
                        send_sms_messages(users_meeting_new, meeting, None, users_data)
                else:
                    start_meeting(users_data)

        def find_matches_2():
            users_data = UserData.objects.filter(availability=True, one_on_one=True)
            if users_data.count() > 1:
                users_meeting = UserMeeting.objects.filter(meeting__active=True).values_list('user_data')
                users_meeting = [x[0] for x in users_meeting]
                users_data = users_data.exclude(pk__in=users_meeting)
                if users_data.count() > 1:
                    start_meeting(users_data)

        find_matches_3()
        find_matches_2()
