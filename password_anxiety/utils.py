# utils.py
from .models import PasswordBehavior, AnxietySurvey
from django.shortcuts import get_object_or_404

def calculate_anxiety_score(responses):
    confidence = responses['confidence']  # Confidence in remembering passwords
    memory_fear = 6 - responses['memory_fear']  # Fear of forgetting passwords (reverse scale)
    user_familiarity = responses.get('user_familiarity', 3)  # A measure of the user's familiarity with password practices, default is 3

    # Weighted formula
    anxiety_score = (confidence * 0.4) + (memory_fear * 0.4) + (user_familiarity * 0.2)
    return anxiety_score

def calculate_password_behavior(user):
    behavior, created = PasswordBehavior.objects.get_or_create(user=user)

    behavior_score = 0

    if behavior.password_reuse:
        behavior_score += 1  # Reusing passwords makes security weaker
    if behavior.password_modification:
        behavior_score -= 0.5  # Modifying passwords slightly improves security
    if behavior.memory_anxiety > 3:
        behavior_score += 0.5  # High anxiety leads to riskier behavior

    # Normalize the score to fit within 0-5
    behavior_score = max(0, min(5, behavior_score))

    return behavior_score
