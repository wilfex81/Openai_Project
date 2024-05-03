import json
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from .models import ConflictResolutionAdvice,FamilyChallenge,MilestoneCelebration,PrayerRequest
from .serializers import FamilyChallengeSerializer
from .views import CustomDevotionPlansAPIView


class ConflictResolutionAdviceAPITests(APITestCase):
    def test_get_advice_with_valid_search_query(self):
        url = reverse('conflict_resolution_advice')
        search_query = "forgiveness" 

        response = self.client.get(url, {'search_query': search_query}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_get_advice_without_search_query(self):
        url = reverse('conflict_resolution_advice')

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class CustomDevotionPlansAPITestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_create_devotion_plan(self):
        view = CustomDevotionPlansAPIView.as_view()
        data = {
            "familyId": "family123",
            "members": [
                {
                    "memberId": "member1",
                    "name": "John",
                    "age": 30,
                    "interests": ["Bible study", "Prayer"],
                    "spiritualMaturityLevel": "Intermediate"
                },
                {
                    "memberId": "member2",
                    "name": "Jane",
                    "age": 25,
                    "interests": ["Worship music", "Serving others"],
                    "spiritualMaturityLevel": "Beginner"
                }
            ]
        }

        request = self.factory.post('/customDevotionPlans', data, format='json')
        response = view(request)

        self.assertEqual(response.status_code, 201)
        self.assertIn("planId", response.data)
        self.assertIn("message", response.data)
        self.assertEqual(response.data["message"], "Devotion plan created successfully.")

    def test_invalid_request_body(self):
        view = CustomDevotionPlansAPIView.as_view()
        data = {
            "members": [
                {
                    "memberId": "member1",
                    "name": "John",
                    "age": 30,
                    "interests": ["Bible study", "Prayer"],
                    "spiritualMaturityLevel": "Intermediate"
                }
            ]
        }

        request = self.factory.post('/customDevotionPlans', data, format='json')
        response = view(request)

        self.assertEqual(response.status_code, 400)


class MilestoneCelebrationsAPITests(APITestCase):
    def setUp(self):
        self.url = reverse('milestone_celebrations')
        self.valid_payload = {
            'familyId': '12345',
            'milestone': {
                'type': 'birthday',
                'date': '2024-04-13',
                'memberName': 'John Doe'
            }
        }
        self.invalid_payload = {
            'familyId': '12345',
            'milestone': {
                'type': 'birthday',
                'date': '2024-04-13'  # Missing 'memberName' field
            }
        }

    def test_submit_milestone(self):
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MilestoneCelebration.objects.count(), 1)
        
    def test_submit_invalid_milestone(self):
        response = self.client.post(self.url, self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(MilestoneCelebration.objects.count(), 0)


class PrayerRequestsAPITests(APITestCase):
    def setUp(self):
        self.url = reverse('prayer_requests')
        self.valid_payload = {
            'familyId': '12345',
            'requestDetails': {
                'request': 'Please pray for healing',
                'date': '2024-04-13'
            }
        }
        self.invalid_payload = {
            'familyId': '12345',
            'requestDetails': {
                'date': '2024-04-13'  # Missing 'request' field
            }
        }

    def test_submit_prayer_request(self):
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PrayerRequest.objects.count(), 1)

    def test_submit_invalid_prayer_request(self):
        response = self.client.post(self.url, self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(PrayerRequest.objects.count(), 0)


class FamilyChallengesAPITests(APITestCase):
    def test_get_challenges_with_valid_keyword(self):
        url = reverse('family_challenges')
        keyword = "family bonding"

        response = self.client.get(url, {'keyword': keyword}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_get_challenges_without_keyword(self):
        url = reverse('family_challenges')

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class FeedbackAPITestCase(APITestCase):
    def test_submit_feedback(self):
        url = reverse('feedback')
        data = {'family_id': 'test_family', 'feedback': 'Test feedback details'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_feedback(self):
        url = reverse('feedback')
        data = {'feedback': 'Test feedback details'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
