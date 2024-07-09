from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.parsers import JSONParser

from clubusers.models import UserProfile, LeaderProfile, FollowerProfile, Availability
from clubusers.serializers import UserProfileSerializer, FollowerProfileSerializer, LeaderProfileSerializer, \
    AvailabilitySerializer


class UserProfileList(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["sex", "timezone"]

    def perform_create(self, serializer):
        # The sequence of running:
        # UserProfileSerializer::validate
        # UserProfileList::perform_create
        # UserProfileSerializer::create
        # print('UserProfileList::perform_create')
        serializer.save(owner=self.request.user)


class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    # permission_classes = [IsOwnerOrReadOnly]


class LeaderProfileList(generics.ListCreateAPIView):
    queryset = LeaderProfile.objects.all()
    serializer_class = LeaderProfileSerializer

    # permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LeaderProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = LeaderProfile.objects.all()
    serializer_class = LeaderProfileSerializer
    # permission_classes = [IsOwnerOrReadOnly]


class FollowerProfileList(generics.ListCreateAPIView):
    queryset = FollowerProfile.objects.all()
    serializer_class = FollowerProfileSerializer

    # permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class FollowerProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = FollowerProfile.objects.all()
    serializer_class = FollowerProfileSerializer
    # permission_classes = [IsOwnerOrReadOnly]


class AvailabilityList(generics.ListCreateAPIView):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer

    # permission_classes = []

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class AvailabilityDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]


@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        username = data.get('username')
        password = data.get('password')
        print(f'username={username} password={password}')
        user = authenticate(username=username, password=password)
        if user is not None:
            return JsonResponse({'status': 'OK'}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'status': f'Error: username={username} password does not match the record'},
                                status=status.HTTP_404_NOT_FOUND)
