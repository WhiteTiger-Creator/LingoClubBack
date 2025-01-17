# Generated by Django 4.2.9 on 2024-03-08 00:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("clubusers", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Meeting",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                (
                    "training_language",
                    models.CharField(
                        choices=[
                            ("EN", "English"),
                            ("ES", "Spanish"),
                            ("CN", "Chinese"),
                        ],
                        default="ES",
                        max_length=2,
                    ),
                ),
                (
                    "base_language",
                    models.CharField(
                        choices=[
                            ("EN", "English"),
                            ("ES", "Spanish"),
                            ("CN", "Chinese"),
                        ],
                        default="EN",
                        max_length=2,
                    ),
                ),
                ("meeting_date", models.DateField()),
                (
                    "meeting_hour",
                    models.IntegerField(
                        choices=[
                            (0, "0"),
                            (1, "1"),
                            (2, "2"),
                            (3, "3"),
                            (4, "4"),
                            (5, "5"),
                            (6, "6"),
                            (7, "7"),
                            (8, "8"),
                            (9, "9"),
                            (10, "10"),
                            (11, "11"),
                            (12, "12"),
                            (13, "13"),
                            (14, "14"),
                            (15, "15"),
                            (16, "16"),
                            (17, "17"),
                            (18, "18"),
                            (19, "19"),
                            (20, "20"),
                            (21, "21"),
                            (22, "22"),
                            (23, "23"),
                        ]
                    ),
                ),
                (
                    "meeting_minute",
                    models.IntegerField(
                        choices=[(0, "0"), (15, "15"), (30, "30"), (45, "45")]
                    ),
                ),
                (
                    "meeting_length",
                    models.IntegerField(
                        choices=[
                            (0, "0"),
                            (15, "15"),
                            (30, "30"),
                            (45, "45"),
                            (60, "60"),
                        ],
                        default=15,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            (
                                "PROPOSED",
                                "The meeting is proposed by a follower and waiting for confirmation from the leader.",
                            ),
                            ("CONFIRMED", "The leader has accepted the meeting."),
                            ("REJECTED", "The leader has rejected the meeting."),
                            (
                                "CANCELLED_BY_LEADER",
                                "The meeting is cancelled by the leader.",
                            ),
                            (
                                "CANCELLED_BY_FOLLOWER",
                                "The meeting is cancelled by the follower.",
                            ),
                            (
                                "COMPLETED_BY_LEADER",
                                "The meeting is reported as completed by the leader",
                            ),
                            (
                                "COMPLETED_BY_FOLLOWER",
                                "The meeting is reported as completed by the follower",
                            ),
                            ("WAITING_FOR_COMPLETED", "waiting for completed."),
                            ("COMPLETED", "The meeting is completed."),
                        ],
                        default="PROPOSED",
                        max_length=30,
                    ),
                ),
                ("zoom_link", models.CharField(blank=True, max_length=300, null=True)),
                (
                    "timezone",
                    models.CharField(
                        choices=[
                            ("PST", "US/Pacific"),
                            ("EST", "US/Eastern"),
                            ("MST", "US/Mountain"),
                            ("CST", "US/Central"),
                        ],
                        default="PST",
                        max_length=3,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("completed_at", models.DateTimeField(blank=True, null=True)),
                ("reported_as_completed_by_leader", models.BooleanField(default=False)),
                (
                    "reported_as_completed_by_follower",
                    models.BooleanField(default=False),
                ),
                ("is_mutable", models.BooleanField(default=True)),
                (
                    "follower",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="clubusers.followerprofile",
                    ),
                ),
                (
                    "leader",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="clubusers.leaderprofile",
                    ),
                ),
            ],
            options={
                "ordering": ["created_at"],
            },
        ),
        migrations.CreateModel(
            name="MeetingReview",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("happened_at", models.DateTimeField(auto_now_add=True, null=True)),
                (
                    "stars",
                    models.IntegerField(
                        choices=[
                            (1, "Very bad"),
                            (2, "Not good."),
                            (3, "It is OK"),
                            (4, "Good"),
                            (5, "Excellent"),
                        ]
                    ),
                ),
                ("comment", models.TextField()),
                (
                    "given_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="given_by",
                        to="clubusers.followerprofile",
                    ),
                ),
                (
                    "given_to",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="given_to",
                        to="clubusers.leaderprofile",
                    ),
                ),
                (
                    "meeting_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="meetings.meeting",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="MeetingEvent",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("field", models.CharField(blank=True, max_length=50, null=True)),
                ("old_value", models.CharField(blank=True, max_length=50, null=True)),
                ("new_value", models.CharField(blank=True, max_length=50, null=True)),
                ("happened_at", models.DateTimeField(auto_now_add=True, null=True)),
                (
                    "major_reason",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("NORMAL", "The status change is normal, as expected."),
                            (
                                "TIME_CONFLICT",
                                "The meeting cannot happen because of time conflict.",
                            ),
                            (
                                "MIND_CHANGED",
                                "Leader or follower changes their mind. Specific reason is not specified.",
                            ),
                            (
                                "REVIEW_RELATED",
                                "Leader or follower is not satisfied with other party's review.",
                            ),
                            ("PAYMENT_RELATED", "not satisfied with the payment term."),
                        ],
                        max_length=30,
                        null=True,
                    ),
                ),
                (
                    "minor_reason",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("DURATION_TOO_LONG", "Scheduled meeting is too long."),
                            ("DURATION_TOO_SHORT", "Scheduled meeting is too short."),
                        ],
                        max_length=30,
                        null=True,
                    ),
                ),
                (
                    "actor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "meeting_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="meetings.meeting",
                    ),
                ),
            ],
        ),
    ]
