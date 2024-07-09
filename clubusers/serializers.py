from rest_framework import serializers

from clubusers.models import UserProfile, LeaderProfile, FollowerProfile, Availability
from rest_framework import permissions


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'first_name', 'last_name', 'password', 'confirm_password', 'email', 'preferred_name', 'date_of_birth', 'timezone', 'sex')
        extra_kwargs = {
            'password': {'write_only': True},  # When GET the record, the field of password will not show up.
            'confirm_password': {'write_only': True},
        }

    def validate(self, data):
        # print(f'UserProfileSerializer::validate')
        for letter in r'(){}[]/\<>':
            if letter in data['password']:
                raise serializers.ValidationError("ERROR: password should not contain special characters, from example: { [ / | < >")
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("ERROR: passwords do not match")
        return data

    def create(self, validated_data):
        # print(f'UserProfileSerializer::create {validated_data}')
        if len(UserProfile.objects.filter(email=validated_data['email'])) == 0:
            user = UserProfile.objects.create(
                username=validated_data['email'],
                email=validated_data['email'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name']
            )
            user.set_password(validated_data['password'])
            user.save()
            return user
        else:
            raise serializers.ValidationError(f"ERROR: email={validated_data['email']} exists already.")


class LeaderProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = LeaderProfile
        fields = ('owner', 'training_language', 'training_language_skill_level', 'introduction',
                  'base_language', 'base_language_skill_level')


class FollowerProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = FollowerProfile
        fields = ('owner', 'training_language', 'training_language_skill_level', 'introduction',
                  'base_language', 'base_language_skill_level')


class AvailabilitySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Availability
        fields = ('owner', 'training_language', 'a0000', 'a0015', 'a0030')

    def validate(self, data):
        if not (bool(data['a0000']) and bool(data['a0015']) and bool(data['a0030'])):
            raise serializers.ValidationError("ERROR: No any time slot is available.")
        return data
