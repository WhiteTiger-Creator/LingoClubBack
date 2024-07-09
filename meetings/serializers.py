from rest_framework import serializers

from meetings.models import Meeting, MeetingEvent, MeetingReview


class MeetingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Meeting
        fields = ('id', 'leader', 'follower', 'training_language', 'base_language', 'meeting_date', 'meeting_hour', 'meeting_minute', 'meeting_length',
                  'status', 'zoom_link', 'timezone',
                  'created_at', 'completed_at', 'is_mutable',
                  'reported_as_completed_by_follower', 'reported_as_completed_by_leader')


class MeetingEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = MeetingEvent
        fields = ('id', 'actor', 'field', 'old_value', 'new_value', 'major_reason', 'minor_reason', 'happened_at')


class MeetingReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = MeetingReview
        fields = ('id', 'given_by', 'given_to', 'stars', 'comment', 'happened_at')
        # fields = ('id', 'given_by', 'stars', 'comment', 'happened_at')
