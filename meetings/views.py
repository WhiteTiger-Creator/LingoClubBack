import pytz
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from meetings.models import Meeting, MEETING_STATUS_CHOICES, MeetingEvent, MeetingReview
from meetings.serializers import MeetingSerializer, MeetingEventSerializer, MeetingReviewSerializer
import datetime as dt
from rest_framework import status

from django.http import HttpResponse

from meetings.utils.send_out_emails import ask_confirmation_to_leader, tell_follower_meeting_rejected_by_leader, \
    send_zoom_link_to_leader_follower, tell_follower_meeting_cancelled_by_leader, tell_leader_meeting_cancelled_by_follower


class MeetingList(generics.ListCreateAPIView):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer
    # permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["leader", "follower", "training_language", "status"]

    def perform_create(self, serializer):
        created_object = serializer.save()
        ask_confirmation_to_leader(created_object)


class MeetingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Must claim That Content-Type: application/json so that type(request.data) id dict.
    # Without Content-Type: application/json, type(request.data) is QueryDict
    def partial_update(self, request, *args, **kwargs):
        original_meeting = self.get_object()
        serializer = self.get_serializer(original_meeting, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # print(serializer.data, type(serializer.data))
        print(serializer.validated_data, type(serializer.validated_data), serializer.validated_data['status'])

        # After "The leader has accepted the meeting", create a zoom link
        new_status = serializer.validated_data.get('status', None)
        # new_status is CONFIRMED
        if original_meeting.status != MEETING_STATUS_CHOICES[1][0] and new_status == MEETING_STATUS_CHOICES[1][0] and original_meeting.zoom_link is not None:
            print('adding zoom meeting.')
            updated_meeting = serializer.save(zoom_link='bbb@zoom', accepted_by_leader_at=dt.datetime.utcnow().astimezone(pytz.UTC))
            send_zoom_link_to_leader_follower(updated_meeting)

        # If the leader rejects the meeting, send an email to the follower to notify
        if original_meeting.status != MEETING_STATUS_CHOICES[2][0] and new_status == MEETING_STATUS_CHOICES[2][0]:
            updated_meeting = serializer.save()
            tell_follower_meeting_rejected_by_leader(updated_meeting)

        return Response(serializer.data)


# def meeting_confirm(request, pk):
#     try:
#         # print('meeting_confirm')
#         meeting = Meeting.objects.get(pk=pk)
#         meeting.status = MEETING_STATUS_CHOICES[1][0]
#         meeting.save()
#         return HttpResponse('OK', status=200)
#     except Exception as error:
#         # print(f'meeting_confirm error={error}')
#         return HttpResponse('Not exist', status=404)
#
#
# def meeting_reject(request, pk):
#     try:
#         # print('meeting_confirm')
#         meeting = Meeting.objects.get(pk=pk)
#         meeting.status = MEETING_STATUS_CHOICES[2][0]
#         meeting.save()
#         return HttpResponse('OK', status=200)
#     except Exception as error:
#         # print(f'meeting_confirm error={error}')
#         return HttpResponse('Not exist', status=404)


class MeetingEventList(generics.ListCreateAPIView):
    # queryset = MeetingEvent.objects.all()
    serializer_class = MeetingEventSerializer
    # permission_classes = [permissions.IsAdminUser]

    def perform_create(self, meetingEventSerializer):
        print('MeetingEventList::perform_create')
        meeting_id = self.kwargs['meeting_id']
        meeting = Meeting.objects.get(id=meeting_id)
        old_status_value = meeting.status
        meeting_event = meetingEventSerializer.save(meeting_id=meeting, old_value=old_status_value)
        print(meeting_event.field.strip().lower(), meeting_event.new_value)

        # If the leader accepts the meeting request, then, create a zoom link and send the email to both of leader and follower.
        # MEETING_STATUS_CHOICES[1][0] == CONFIRMED
        if meeting_event.field.strip().lower() == 'status' and meeting_event.new_value.strip().lower() == MEETING_STATUS_CHOICES[1][0].strip().lower():
            print(f'MeetingEventList::perform_create: meeting.status={meeting.status}  meeting.zoom_link={meeting.zoom_link}')
            if meeting.status != MEETING_STATUS_CHOICES[1][0] and meeting.zoom_link is not None:
                print('adding zoom meeting.')
                meeting.zoom_link = 'bbb@zoom'
                meeting.accepted_by_leader_at = dt.datetime.utcnow().astimezone(pytz.UTC)
                meeting.status = MEETING_STATUS_CHOICES[1][0]
                meeting.save()
                print('The meeting status is updated.')
                send_zoom_link_to_leader_follower(meeting)
                print('Sent out emmails to both of leader and follower')

        # If the leader rejects the meeting request, then, send the email to both of leader and follower.
        # MEETING_STATUS_CHOICES[2][0] == REJECTED
        if meeting_event.field.strip().lower() == 'status' and meeting_event.new_value.strip().lower() == MEETING_STATUS_CHOICES[2][0].strip().lower():
            print(f'MeetingEventList::perform_create: meeting.status={meeting.status}')
            if meeting.status != MEETING_STATUS_CHOICES[2][0]:
                print('The meeting is rejected by the leader.')
                meeting.status = MEETING_STATUS_CHOICES[2][0]
                meeting.is_mutable = False
                meeting.save()
                print('The meeting status is updated.')
                tell_follower_meeting_rejected_by_leader(meeting)
                print('tell_follower_meeting_rejected_by_leader')

        # If the leader cancels the meeting request after the meeting has been accepted, then, send the email to follower.
        # MEETING_STATUS_CHOICES[3][0] == CANCELLED_BY_LEADER
        if meeting_event.field.strip().lower() == 'status' and meeting_event.new_value.strip().lower() == MEETING_STATUS_CHOICES[3][0].strip().lower():
            print(f'MeetingEventList::perform_create: meeting.status={meeting.status}')
            if meeting.status != MEETING_STATUS_CHOICES[3][0]:
                print('The meeting is cancelled by the leader.')
                meeting.status = MEETING_STATUS_CHOICES[3][0]
                meeting.is_mutable = False
                meeting.save()
                print('The meeting status is updated.')
                tell_follower_meeting_cancelled_by_leader(meeting, meeting_event.major_reason)
                print('tell_follower_meeting_cancelled_by_leader')

        # If the follower cancels the meeting request after the meeting has been accepted, then, send the email to leader.
        # MEETING_STATUS_CHOICES[4][0] == CANCELLED_BY_FOLLOWER
        if meeting_event.field.strip().lower() == 'status' and meeting_event.new_value.strip().lower() == MEETING_STATUS_CHOICES[4][0].strip().lower():
            print(f'MeetingEventList::perform_create: meeting.status={meeting.status}')
            if meeting.status != MEETING_STATUS_CHOICES[4][0]:
                print('The meeting is cancelled by the follower.')
                meeting.status = MEETING_STATUS_CHOICES[4][0]
                meeting.is_mutable = False
                meeting.save()
                print('The meeting status is updated.')
                tell_leader_meeting_cancelled_by_follower(meeting, meeting_event.major_reason)
                print('tell_leader_meeting_cancelled_by_follower')

        # After the meeting is reported as completed by a leader.
        # MEETING_STATUS_CHOICES[5][0] == COMPLETED_BY_LEADER
        if meeting_event.field.strip().lower() == 'status' and meeting_event.new_value.strip().lower() == MEETING_STATUS_CHOICES[5][0].strip().lower():
            print(f'MeetingEventList::perform_create: meeting.status={meeting.status}')
            if meeting.status != MEETING_STATUS_CHOICES[5][0]:
                print('the meeting is reported as completed by a leader')
                if meeting.reported_as_completed_by_follower is True:  # Both of leader and follower report as completed.
                    meeting.status = MEETING_STATUS_CHOICES[-1][0]  # MEETING_STATUS_CHOICES[-1][0] == COMPLETED
                    meeting.is_mutable = False
                else:
                    meeting.status = MEETING_STATUS_CHOICES[5][0]
                meeting.reported_as_completed_by_leader = True
                meeting.save()


        # After the meeting is reported as completed by a follower.
        # MEETING_STATUS_CHOICES[6][0] == COMPLETED_BY_FOLLOWER
        if meeting_event.field.strip().lower() == 'status' and meeting_event.new_value.strip().lower() == MEETING_STATUS_CHOICES[6][0].strip().lower():
            print(f'MeetingEventList::perform_create: meeting.status={meeting.status}')
            if meeting.status != MEETING_STATUS_CHOICES[6][0]:
                print('the meeting is reported as completed by a follower')
                if meeting.reported_as_completed_by_leader is True:  # Both of leader and follower report as completed.
                    meeting.status = MEETING_STATUS_CHOICES[-1][0]  # MEETING_STATUS_CHOICES[-1][0] == COMPLETED
                    meeting.is_mutable = False
                else:
                    meeting.status = MEETING_STATUS_CHOICES[6][0]
                meeting.reported_as_completed_by_follower = True
                meeting.save()

    def get_queryset(self):
        meeting_id = self.kwargs['meeting_id']
        print(f'MeetingEventList::get_queryset meeting_id={meeting_id}')
        return MeetingEvent.objects.filter(meeting_id=meeting_id)

    def list(self, request, *args, **kwargs):
        print(f'MeetingEventList::list')
        try:
            data = self.get_queryset()
        except Exception as error:
            return Response('wrong meeting_id', status=404)

        try:
            serializer = self.get_serializer(data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            context = {'error': str(error), 'success': "false", 'message': 'Failed To Get contents.'}
            return Response(context, status=500)


class MeetingEventDetail(generics.RetrieveUpdateDestroyAPIView):
    # queryset = MeetingEvent.objects.all()
    serializer_class = MeetingEventSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        meeting_id = self.kwargs['meeting_id']
        print(f'MeetingEventDetail::get_queryset: meeting_id={meeting_id}')
        return MeetingEvent.objects.filter(meeting_id=meeting_id)

    def partial_update(self, request, *args, **kwargs):
        print('MeetingEventDetail::partial_update')
        original_meeting_event = self.get_object()
        serializer = self.get_serializer(original_meeting_event, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        print('partial update', original_meeting_event.status)
        return Response(serializer.data)


class MeetingReviewList(generics.ListCreateAPIView):
    # queryset = MeetingEvent.objects.all()
    serializer_class = MeetingReviewSerializer
    # permission_classes = [permissions.IsAdminUser]

    def perform_create(self, meetingReviewSerializer):
        print('MeetingReviewList::perform_create')
        meeting_id = self.kwargs['meeting_id']
        meeting = Meeting.objects.get(id=meeting_id)
        meetingReviewSerializer.save(meeting_id=meeting)

    def get_queryset(self):
        meeting_id = self.kwargs['meeting_id']
        print(f'MeetingReviewList::get_queryset meeting_id={meeting_id}')
        return MeetingReview.objects.filter(meeting_id=meeting_id)

    def list(self, request, *args, **kwargs):
        print(f'MeetingReviewList::list')
        try:
            data = self.get_queryset()
        except Exception as error:
            print(f'MeetingReviewList::list: error={error}')
            return Response('wrong meeting_id', status=404)

        try:
            meeting_review_serializer = self.get_serializer(data, many=True)
            return Response(meeting_review_serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            context = {'error': str(error), 'success': "false", 'message': 'Failed To Get contents.'}
            return Response(context, status=500)


class MeetingReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    # queryset = MeetingEvent.objects.all()
    serializer_class = MeetingReviewSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        meeting_id = self.kwargs['meeting_id']
        print(f'MeetingReviewDetail::get_queryset: meeting_id={meeting_id}')
        return MeetingEvent.objects.filter(meeting_id=meeting_id)

    def partial_update(self, request, *args, **kwargs):
        print('MeetingReviewDetail::partial_update')
        original_meeting_review = self.get_object()
        meeting_review_serializer = self.get_serializer(original_meeting_review, data=request.data, partial=True)
        if not meeting_review_serializer.is_valid():
            return Response(meeting_review_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        print('MeetingReviewDetail:partial update', original_meeting_review.status)
        return Response(meeting_review_serializer.data)

