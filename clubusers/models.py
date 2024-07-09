from django.contrib.auth.models import AbstractUser
from django.db import models


# The 1st choice will be displayed as the default choice in the default html page.
TIMEZONE_CHOICES = [
    ("PST", "US/Pacific"),
    ("EST", "US/Eastern"),
    ("MST", "US/Mountain"),
    ("CST", "US/Central"),
]

SEX_CHOICES = [
    ("U", "Undisclosed"),
    ("M", "male"),
    ("F", "female"),
]

LANGUAGE_CHOICES = [
    ("EN", "English"),
    ("ES", "Spanish"),
    ("CN", "Chinese"),
]

LANGUAGE_SKILL_LEVEL_CHOICES = [
    (1, "Beginner"),
    (2, "Know a little"),
    (3, "Intermediate"),
    (4, "Fluent speaker"),
    (5, "Native speaker"),
]


# https://docs.djangoproject.com/en/4.1/topics/auth/customizing/#substituting-a-custom-user-model
# https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html
# MUST: AUTH_USER_MODEL = 'clubusers.UserProfile' in settings.py
class UserProfile(AbstractUser):
    # a few default values have been defined by AbstractUser, for example, username, password, firstname, lastname, date_joined and email so no need to do it here.
    # Setting blank=True means that a field is not required when a form is submitted, allowing users to leave it empty without triggering a validation error
    # When you set null=True, you’re telling Django that the database should allow this field to have empty or missing values, typically represented as NULL in the database.
    preferred_name = models.CharField(max_length=200, null=True, blank=True)  # Must provide a preferred_name to display in User Profile
    date_of_birth = models.DateField(null=True, blank=True)  # So that we can calculate how old the user is and display the age in User Profile
    timezone = models.CharField(max_length=3, choices=TIMEZONE_CHOICES, default='PST')  # To adjust availability
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, default='U')
    confirm_password = models.CharField(max_length=200, null=True, blank=True)


class LeaderProfile(models.Model):
    owner_language = models.CharField(max_length=152, primary_key=True)  # the key is username_languageCode: username_CN
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    training_language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='ES')  # required field
    training_language_skill_level = models.IntegerField(choices=LANGUAGE_SKILL_LEVEL_CHOICES)  # required field
    introduction = models.TextField()  # leaders must provide intro
    base_language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='EN') # required field
    base_language_skill_level = models.IntegerField(choices=LANGUAGE_SKILL_LEVEL_CHOICES)  # required field

    def save(self, *args, **kwargs):
        self.owner_language = str(self.owner) + '_' + str(self.training_language)
        super(LeaderProfile, self).save(*args, **kwargs)


class FollowerProfile(models.Model):
    owner_language = models.CharField(max_length=152, primary_key=True)  # the key is username_languageCode: username_CN
    owner = models.ForeignKey(UserProfile, related_name='follower_profile', on_delete=models.CASCADE)
    training_language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='ES')  # required field
    training_language_skill_level = models.IntegerField( choices=LANGUAGE_SKILL_LEVEL_CHOICES)  # required field
    introduction = models.TextField(null=True, blank=True)  # followers may not provide intro
    base_language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='EN')  # required field
    base_language_skill_level = models.IntegerField(choices=LANGUAGE_SKILL_LEVEL_CHOICES)  # required field

    def save(self, *args, **kwargs):
        self.owner_language = str(self.owner) + '_' + str(self.training_language)
        super(FollowerProfile, self).save(*args, **kwargs)


class Availability(models.Model):
    owner_language = models.CharField(max_length=152, primary_key=True)  # the key is username_languageCode: username_CN
    training_language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='ES')  # required field
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    a0000 = models.BooleanField(default=False)
    a0015 = models.BooleanField(default=False)
    a0030 = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.owner_language = str(self.owner) + '_' + str(self.training_language)
        super(Availability, self).save(*args, **kwargs)
