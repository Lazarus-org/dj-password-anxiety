from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .models import AnxietySurvey, PasswordBehavior
from .serializers import AnxietySurveyCreateSerializer, AnxietySurveySerializer, PasswordBehaviorSerializer
from .utils import calculate_anxiety_score, calculate_password_behavior

class AnxietySurveyCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AnxietySurveyCreateSerializer

    def create(self, request, *args, **kwargs):
        # Pass data to the serializer
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Call the serializer's create method to handle both anxiety survey and password behavior
            result = serializer.save()


            anxiety_survey = result.get("anxiety_survey")
            password_behavior = result.get("password_behavior")
            data = {
                "anxiety_survey": AnxietySurveySerializer(anxiety_survey).data,
                "password_behavior": PasswordBehaviorSerializer(password_behavior).data
            }
            # Return the response with the data from the serializer
            return Response(data=data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


    def get_serializer_context(self):
        return {
            "request": self.request,
            "user": self.request.user
        }