from django.db import models
from clubusers.models import LeaderProfile, FollowerProfile, UserProfile
from clubusers.models import LANGUAGE_CHOICES, TIMEZONE_CHOICES
import uuid

MEETING_STATUS_CHOICES = [
    ("PROPOSED", "The meeting is proposed by a follower and waiting for confirmation from the leader."),
    ("CONFIRMED", "The leader has accepted the meeting."),
    ("REJECTED", "The leader has rejected the meeting."),
    ("CANCELLED_BY_LEADER", "The meeting is cancelled by the leader."),
    ("CANCELLED_BY_FOLLOWER", "The meeting is cancelled by the follower."),
    ("COMPLETED_BY_LEADER", "The meeting is reported as completed by the leader"),
    ("COMPLETED_BY_FOLLOWER", "The meeting is reported as completed by the follower"),
    ("WAITING_FOR_COMPLETED", "waiting for completed."),
    ("COMPLETED", "The meeting is completed."),
]

MAJOR_REASON_OF_MEETING_STATUS_CHANGE_CHOICES = [
    ("NORMAL", "The status change is normal, as expected."),
    ("TIME_CONFLICT", "The meeting cannot happen because of time conflict."),
    ("MIND_CHANGED", "Leader or follower changes their mind. Specific reason is not specified."),
    ("REVIEW_RELATED", "Leader or follower is not satisfied with other party's review."),
    ("PAYMENT_RELATED", "not satisfied with the payment term."),
]

MINOR_REASON_OF_MEETING_STATUS_CHANGE_CHOICES = [
    ("DURATION_TOO_LONG", "Scheduled meeting is too long."),
    ("DURATION_TOO_SHORT", "Scheduled meeting is too short."),
]

REVIEW_CHOICES = [
    (1, "Very bad"),
    (2, "Not good."),
    (3, "It is OK"),
    (4, "Good"),
    (5, "Excellent"),
]

MEETING_HOUR_CHOICES = [(x, str(x)) for x in range(24)]
MEETING_MINUTE_CHOICES = [(x, str(x)) for x in [0, 15, 30, 45]]
MEETING_LENGTH_CHOICES = [(x, str(x)) for x in [0, 15, 30, 45, 60]]


class Meeting(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    leader = models.ForeignKey(LeaderProfile, on_delete=models.CASCADE)
    follower = models.ForeignKey(FollowerProfile, on_delete=models.CASCADE)
    training_language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='ES')  # required field
    base_language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='EN')  # required field
    meeting_date = models.DateField()
    meeting_hour = models.IntegerField(choices=MEETING_HOUR_CHOICES)
    meeting_minute = models.IntegerField(choices=MEETING_MINUTE_CHOICES)
    meeting_length = models.IntegerField(choices=MEETING_LENGTH_CHOICES, default=15)
    status = models.CharField(max_length=30, choices=MEETING_STATUS_CHOICES, default='PROPOSED')  # required field
    zoom_link = models.CharField(max_length=300, null=True, blank=True)
    timezone = models.CharField(max_length=3, choices=TIMEZONE_CHOICES, default='PST')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    reported_as_completed_by_leader = models.BooleanField(default=False)
    reported_as_completed_by_follower = models.BooleanField(default=False)
    is_mutable = models.BooleanField(default=True)

    # After 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination', see the following error
    # UnorderedObjectListWarning: Pagination may yield inconsistent results with an unordered object_list
    # This will solve the issue.
    class Meta:
        ordering = ['created_at']


class MeetingEvent(models.Model):
    meeting_id = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    actor = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    field = models.CharField(max_length=50, null=True, blank=True)
    old_value = models.CharField(max_length=50, null=True, blank=True)
    new_value = models.CharField(max_length=50, null=True, blank=True)
    happened_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    major_reason = models.CharField(max_length=30, choices=MAJOR_REASON_OF_MEETING_STATUS_CHANGE_CHOICES, null=True, blank=True)
    minor_reason = models.CharField(max_length=30, choices=MINOR_REASON_OF_MEETING_STATUS_CHANGE_CHOICES, null=True, blank=True)


class MeetingReview(models.Model):
    meeting_id = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    given_by = models.ForeignKey(FollowerProfile, on_delete=models.CASCADE, related_name="given_by")
    given_to = models.ForeignKey(LeaderProfile, on_delete=models.CASCADE, related_name="given_to")
    happened_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    stars = models.IntegerField(choices=REVIEW_CHOICES)
    comment = models.TextField()
