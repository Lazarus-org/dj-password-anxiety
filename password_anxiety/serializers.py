from rest_framework import serializers
from .models import AnxietySurvey, PasswordBehavior
from .utils import calculate_anxiety_score, calculate_password_behavior

class AnxietySurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = AnxietySurvey
        fields = ['confidence_score', 'anxiety_level', 'date_taken']

class PasswordBehaviorSerializer(serializers.ModelSerializer):
    class Meta:
        model = PasswordBehavior
        fields = ['password_reuse', 'password_modification', 'memory_anxiety', 'password_behavior_score']



class AnxietySurveyCreateSerializer(serializers.Serializer):
    confidence = serializers.IntegerField(min_value=1, max_value=5, write_only=True)
    memory_fear = serializers.IntegerField(min_value=1, max_value=5, write_only=True)
    user_familiarity = serializers.IntegerField(min_value=1, max_value=5, required=False, write_only=True)
    
    password_reuse = serializers.BooleanField(write_only=True)
    password_modification = serializers.BooleanField(write_only=True)

    anxiety_survey = AnxietySurveySerializer(read_only=True)
    password_behavior = PasswordBehaviorSerializer(read_only=True)

    def validate(self, data):
        if 'user_familiarity' not in data:
            data['user_familiarity'] = 3
        return data

    def create(self, validated_data):
        user = self.context['request'].user

        # Calculate anxiety score
        anxiety_score = calculate_anxiety_score(validated_data)

        # Update or create AnxietySurvey record
        survey, _ = AnxietySurvey.objects.update_or_create(
            user=user,
            defaults={
                'confidence_score': validated_data['confidence'],
                'anxiety_level': anxiety_score
            }
        )

        # Update or create PasswordBehavior with user inputs
        password_behavior, _ = PasswordBehavior.objects.update_or_create(
            user=user,
            defaults={
                'password_reuse': validated_data['password_reuse'],
                'password_modification': validated_data['password_modification'],
                'memory_anxiety': anxiety_score
            }
        )

        # Calculate password behavior score based on new data
        password_behavior_score = calculate_password_behavior(user)
        password_behavior.password_behavior_score = password_behavior_score
        password_behavior.save()

        return {
            'anxiety_survey': survey,
            'password_behavior': password_behavior
        }