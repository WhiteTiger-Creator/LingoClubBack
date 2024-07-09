from lingoclub.settings import EARNING_RATE_PER_HOUR, DEFAULT_FROM_EMAIL
from django.template.loader import get_template
from django.core.mail import EmailMessage


def ask_confirmation_to_leader(meeting_object):
    # print(f'send out email to ask for confirmation. {created_object.leader.owner.email}')
    message = get_template("meetings/ask_confirmation_to_leader.html").render(
        {
            'meeting': meeting_object,
            'earning': meeting_object.meeting_length / 60 * EARNING_RATE_PER_HOUR
        }
    )
    mail = EmailMessage(
        subject='lingoClub.org: someone wants to practice Spanish with you',
        body=message,
        from_email=DEFAULT_FROM_EMAIL,
        to=[f'{meeting_object.leader.owner.email}'],
        reply_to=[DEFAULT_FROM_EMAIL],
    )
    mail.content_subtype = "html"
    mail.send()


def tell_follower_meeting_rejected_by_leader(meeting_object):
    message = get_template("meetings/tell_follower_meeting_rejected_by_leader.html").render(
        {
            'meeting': meeting_object,
        }
    )
    mail = EmailMessage(
        subject='lingoClub.org: your meeting request was rejected by a lingo leader.',
        body=message,
        from_email=DEFAULT_FROM_EMAIL,
        to=[f'{meeting_object.follower.owner.email}'],
        reply_to=[DEFAULT_FROM_EMAIL],
    )
    mail.content_subtype = "html"
    mail.send()


def tell_follower_meeting_cancelled_by_leader(meeting_object, reason):
    message = get_template("meetings/tell_follower_meeting_cancelled_by_leader.html").render(
        {
            'meeting': meeting_object,
            'reason': reason
        }
    )
    mail = EmailMessage(
        subject='lingoClub.org: your scheduled meeting was cancelled by a lingo leader.',
        body=message,
        from_email=DEFAULT_FROM_EMAIL,
        to=[f'{meeting_object.follower.owner.email}'],
        reply_to=[DEFAULT_FROM_EMAIL],
    )
    mail.content_subtype = "html"
    mail.send()


def tell_leader_meeting_cancelled_by_follower(meeting_object, reason):
    message = get_template("meetings/tell_leader_meeting_cancelled_by_follower.html").render(
        {
            'meeting': meeting_object,
            'reason': reason
        }
    )
    mail = EmailMessage(
        subject='lingoClub.org: your scheduled meeting was cancelled by a lingo follower.',
        body=message,
        from_email=DEFAULT_FROM_EMAIL,
        to=[f'{meeting_object.leader.owner.email}'],
        reply_to=[DEFAULT_FROM_EMAIL],
    )
    mail.content_subtype = "html"
    mail.send()


def send_zoom_link_to_leader_follower(meeting_object):
    # print(f'send out email to ask for confirmation. {created_object.leader.owner.email}')
    message = get_template("meetings/send_zoom_link_to_leader_follower.html").render(
        {
            'meeting': meeting_object,
            'earning': meeting_object.meeting_length / 60 * EARNING_RATE_PER_HOUR
        }
    )
    mail = EmailMessage(
        subject='lingoClub.org: The Zoom meeting link is available!',
        body=message,
        from_email=DEFAULT_FROM_EMAIL,
        to=[f'{meeting_object.leader.owner.email}', f'{meeting_object.follower.owner.email}'],
        reply_to=[DEFAULT_FROM_EMAIL],
    )
    mail.content_subtype = "html"
    mail.send()

