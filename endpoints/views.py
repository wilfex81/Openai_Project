import os
import logging
import requests
from decouple import config
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework import status
from .serializers import (custom_devotion_plan_schema,milestone_celebration_schema,
                          prayer_request_schema, feedback_schema)
from .serializers import (CustomDevotionPlanSerializer,
                          MilestoneCelebrationSerializer, PrayerRequestSerializer,
                          FeedbackSerializer)

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

openai_api_key = settings.OPENAI_API_KEY

class ConflictResolutionAdviceAPIView(APIView):
    """
    API endpoint to provide conflict resolution advice based on biblical principles.
    """
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('search_query', openapi.IN_QUERY, type=openapi.TYPE_STRING,
                              description='Search query related to the conflict.'),
        ],
        responses={
            200: "Returns a list of advice snippets.",
            404: "No advice found for the given search query."
        },
    )
    def get(self, request):
        """
         Retrieves advice based on search queries related to the conflict.
        """
        search_query = request.query_params.get('search_query', None)
        if not search_query:
            raise NotFound(detail="No search query provided.")

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {openai_api_key}',
        }
        
        logger.info("Request Headers: %s", headers)
        prompt = f"Provide conflict resolution advice related to '{search_query}'. Consider how the parties involved can communicate effectively, understand each other's perspectives, and find compromises."

        data = {
            'model': 'gpt-3.5-turbo-instruct',
            'prompt': prompt,
            'max_tokens': 200,
            'n': 3,
            'temperature': 0.7,
            'top_p': 0.9,
        }

        response = requests.post('https://api.openai.com/v1/completions', headers=headers, json=data)
        
        if response.status_code == 200:
            advice_snippets = [choice['text'].strip().split('. ', 1)[-1] for choice in response.json()['choices']]
            if not advice_snippets:
                raise NotFound(detail="No advice found for the given search query or you are missing openai Key.")
            return Response(advice_snippets, status=status.HTTP_200_OK)
        else:
            raise NotFound(detail="No advice found for the given search query or you are missing openai Key.")


class CustomDevotionPlansAPIView(APIView):
    """
    API endpoint to create customizable devotion plans for families.
    """

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('specific_needs', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=True, description='Specific needs of the family members.'),
            openapi.Parameter('interests', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=True, description='Interests of the family members.'),
            openapi.Parameter('spiritual_maturity_levels', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=True, description='Spiritual maturity levels of the family members.')
        ],
        responses={
            200: "Devotion plan generated successfully.",
            400: "Bad request if the query parameters are missing or invalid."
        }
    )
    def get(self, request):
        """
        Generates a customized devotion plan for a family based on query parameters.
        """
        specific_needs = request.query_params.get('specific_needs', '')
        interests = request.query_params.get('interests', '')
        spiritual_maturity_levels = request.query_params.get('spiritual_maturity_levels', '')

        if not (specific_needs and interests and spiritual_maturity_levels):
            return Response({'error': "Missing required query parameters."}, status=status.HTTP_400_BAD_REQUEST)

        prompt = f"""Create a customized devotion plan based on the specific needs, interests, and spiritual maturity levels of different family members:
        - Specific Needs: {specific_needs}
        - Interests: {interests}
        - Spiritual Maturity Levels: {spiritual_maturity_levels}
        This personalization aims to make devotions more relevant and engaging for everyone involved."""

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {openai_api_key}',
        }
        data = {
            'model': 'gpt-3.5-turbo-instruct',
            'prompt': prompt,
            'max_tokens': 200,
            'n': 3,
            'temperature': 0.7,
            'top_p': 0.9,
        }

        response = requests.post('https://api.openai.com/v1/completions', headers=headers, json=data)
        if response.status_code == 200:
            devotion_plans = [choice['text'].strip().split('. ', 1)[-1] for choice in response.json()['choices']]
            if not devotion_plans:
                raise NotFound(detail="No customized devotion found for the given search params or you are missing openai Key.")
            return Response(devotion_plans, status=status.HTTP_200_OK)
        else:
            raise NotFound(detail="Failed to generate a customized devotion plan or you are missing openai Key.")


class MilestoneCelebrationsAPIView(APIView):
    """
    API endpoint to submit milestone celebrations for families.
    """

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('milestoneType', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=True, description='Type of milestone (e.g., birthday, anniversary, baptism).'),
            openapi.Parameter('milestoneDate', openapi.IN_QUERY, type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, required=True, description='Date of the milestone.'),
            openapi.Parameter('memberName', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=True, description='Name of the family member associated with the milestone.')
        ],
        responses={
            201: "Milestone submitted successfully."
        }
    )
    def get(self, request):
        """
        Submits a family milestone to be celebrated.
        """
        milestone_type = request.query_params.get('milestoneType', '')
        milestone_date = request.query_params.get('milestoneDate', '')
        member_name = request.query_params.get('memberName', '')

        if not (milestone_type and milestone_date and member_name):
            return Response({'error': "Missing required fields in the request data."}, status=status.HTTP_400_BAD_REQUEST)

        prompt = f"Recognize and celebrate the '{milestone_type}' milestone for {member_name} on {milestone_date}.\
            Generate special prayers or devotions for this milestone."

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {openai_api_key}',
        }


        data = {
            'model': 'gpt-3.5-turbo-instruct',
            'prompt': prompt,
            'max_tokens': 200,
            'n': 3,
            'temperature': 0.7,
            'top_p': 0.9,
        }

        response = requests.post('https://api.openai.com/v1/completions', headers=headers, json=data)
        
        if response.status_code == 200:
            milestone_celebration = [choice['text'].strip().split('. ', 1)[-1] for choice in response.json()['choices']]
            if not milestone_celebration:
                raise NotFound(detail="No special prayers or devotions for the given milestone or you are missing openaai Key")
            return Response(milestone_celebration, status=status.HTTP_200_OK)
        else:
            raise Exception("Failed to generate special prayers or devotions or you are missing openai Key.")


class PrayerRequestsAPIView(APIView):
    """
    API endpoint to submit prayer requests for families.
    """

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('requestDetails', openapi.IN_QUERY, type=openapi.TYPE_STRING,  required=True, description='Details of the prayer request.')
        ],
        responses={
            201: "Prayer request submitted successfully."
        }
    )
    def get(self, request):
        """
        Submits a prayer request for a family or family member.
        """
        request_details = request.query_params.get('requestDetails', '')

        if not request_details:
            return Response({'error': "Missing required query parameters."}, status=status.HTTP_400_BAD_REQUEST)

        prompt = f"Provide a prayer for this request '{request_details}'."

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {openai_api_key}',
        }

        data = {
            'model': 'gpt-3.5-turbo-instruct',
            'prompt': prompt,
            'max_tokens': 200,
            'n': 3,
            'temperature': 0.7,
            'top_p': 0.9,
        }

        response = requests.post('https://api.openai.com/v1/completions', headers=headers, json=data)
        
        if response.status_code == 200:
            prayer = [choice['text'].strip().split('. ', 1)[-1] for choice in response.json()['choices']]
            if not prayer:
                raise NotFound(detail="No prayers were generated for the given request or you are missing openai key")
            return Response(prayer, status=status.HTTP_200_OK)
        else:
            raise Exception("Failed to generate prayer or you are missing openai Key.")

    
class FamilyChallengesAPIView(APIView):
    """
    API endpoint to retrieve interactive family challenges.
    """
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('keyword', openapi.IN_QUERY, type=openapi.TYPE_STRING,
                              description='Keyword related to the challenges.')
        ],
        responses={
            200: "Returns a list of challenges.",
            404: "No challenges found for the given keyword."
        }
    )
    def get(self, request):
        """
        Retrieves a list of challenges based on the keyword
        """
        keyword = request.query_params.get('keyword', None)
        if not keyword:
            raise NotFound(detail="No keyword provided.")

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {openai_api_key}',
        }

        prompt = f"List some family challenges related to '{keyword}' focusing on acts of service, kindness, and faith-building activities."

        data = {
            'model': 'gpt-3.5-turbo-instruct',
            'prompt': prompt,
            'max_tokens': 100,
            'n': 3,
        }
        response = requests.post('https://api.openai.com/v1/completions', headers=headers, json=data)
        if response.status_code == 200:
            challenges = [choice['text'].strip().split('. ', 1)[-1] for choice in response.json()['choices']]
            if not challenges:
                raise NotFound(detail="No challenges found for the given keyword or you are missing openai key.")
            return Response(challenges, status=status.HTTP_200_OK)
        else:
            raise NotFound(detail="No challenges found for the given keyword or you are missing openai Key.")
    
    
    

class FeedbackAPIView(APIView):
    """
    API endpoint to submit feedback from families.
    """

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('experiences', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=True, description='Experiences shared by the family.'),
            openapi.Parameter('suggested_topics', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=True, description='Topics suggested by the family.'),
            openapi.Parameter('insights', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=True, description='Insights into the spiritual journey provided by the family.')
        ],
        responses={
            200: "Feedback response generated successfully.",
            400: "Bad request if the query parameters are missing or invalid."
        }
    )
    def get(self, request):
        """
        Generates a response based on the feedback from families.
        """
        experiences = request.query_params.get('experiences', '')
        suggested_topics = request.query_params.get('suggested_topics', '')
        insights = request.query_params.get('insights', '')

        if not (experiences and suggested_topics and insights):
            return Response({'error': "Missing required query parameters."}, status=status.HTTP_400_BAD_REQUEST)

        prompt = f"""Based on the feedback provided by the family:
        Experiences: {experiences}
        Suggested Topics: {suggested_topics}
        Insights: {insights}
        Generate a response that addresses their feedback and provides insights or guidance."""

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {openai_api_key}',
        }

        data = {
            'model': 'gpt-3.5-turbo-instruct',
            'prompt': prompt,
            'max_tokens': 200,
            'n': 3,
            'temperature': 0.7,
            'top_p': 0.9,
        }

        response = requests.post('https://api.openai.com/v1/completions', headers=headers, json=data)
        
        if response.status_code == 200:
            feedback = [choice['text'].strip().split('. ', 1)[-1] for choice in response.json()['choices']]
            if not feedback:
                raise NotFound(detail="No feedback found for the given parameters or you are missing openai Key.")
            return Response(feedback, status=status.HTTP_200_OK)
        else:
            raise Exception("Failed to generate a response based on the feedback or you are missing openai Key.")



