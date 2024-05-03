from django.urls import path
from .views import (ConflictResolutionAdviceAPIView,MilestoneCelebrationsAPIView, 
                    PrayerRequestsAPIView, CustomDevotionPlansAPIView,FamilyChallengesAPIView,
                    FeedbackAPIView)


urlpatterns = [
    path('conflictResolutionAdvice/', ConflictResolutionAdviceAPIView.as_view(), name= 'conflict_resolution_advice'),
    path('customDevotionPlans/', CustomDevotionPlansAPIView.as_view(), name='custom_devotion_plans'),
    path('milestoneCelebrations/', MilestoneCelebrationsAPIView.as_view(), name='milestone_celebrations'),
    path('prayerRequests/', PrayerRequestsAPIView.as_view(), name='prayer_requests'),
    path('familyChallenges/', FamilyChallengesAPIView.as_view(), name='family_challenges'),
    path('feedback/', FeedbackAPIView.as_view(), name='feedback')
]
