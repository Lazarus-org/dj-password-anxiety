from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils import timezone


User = settings.AUTH_USER_MODEL

class PasswordBehavior(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, 
                             db_comment=_("The user who owns this password behavior record"))
    password_reuse = models.BooleanField(
        default=False,
        help_text=_("Indicates if the user reused a password."),
        db_comment=_("Whether the user reused a password")
    )
    password_modification = models.BooleanField(
        default=False,
        help_text=_("Indicates if the user modified their password."),
        db_comment=_("Whether the user modified their password")
    )
    memory_anxiety = models.IntegerField(
        null=True,
        blank=True,
        help_text=_("Rate from 1 (low) to 5 (high) how anxious the user feels about remembering passwords."),
        db_comment=_("User's self-reported anxiety about remembering passwords (1-5)"),
    )
    password_behavior_score = models.FloatField(
        null=True,
        blank=True,
        help_text=_("Calculated score reflecting the user's overall password behavior"),
        db_comment=_("Calculated score reflecting the user's overall password behavior")
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        db_comment=_("Timestamp when the record was created")
        )

    def __str__(self):
        return f"{self.user} - Reuse: {self.password_reuse}, Mod: {self.password_modification}, Score: {self.password_behavior_score}"


class AnxietySurvey(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        db_comment=_("The user who took the anxiety survey")
    )
    confidence_score = models.FloatField(
        help_text=_("Confidence level in remembering passwords, rated from 1 (low) to 5 (high)."),
        db_comment=_("Confidence score (1-5) in remembering passwords")
    )
    anxiety_level = models.FloatField(
        help_text=_("Computed anxiety score based on confidence score and other factors."),
        db_comment=_("Calculated anxiety level, which can be based on a formula"),
        null=True, blank=True
    )
    date_taken = models.DateTimeField(
        auto_now_add=True,
        db_comment=_("Date and time when the survey was taken")
    )

    def __str__(self):
        return f"{self.user} - Anxiety Survey"

