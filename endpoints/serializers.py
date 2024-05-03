from rest_framework import serializers
from drf_yasg import openapi
from .models import (ConflictResolutionAdvice,CustomDevotionPlan, 
                     MilestoneCelebration, PrayerRequest,
                     FamilyMember, MilestoneCelebration, 
                     PrayerRequest, FamilyChallenge,Feedback)




class ConflictResolutionAdviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConflictResolutionAdvice
        fields = ['keyword', 'advice']

class FamilyMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = FamilyMember
        fields = ['memberId', 'name', 'age', 'interests', 'spiritualMaturityLevel']

class CustomDevotionPlanSerializer(serializers.ModelSerializer):
    members = FamilyMemberSerializer(many=True)

    class Meta:
        model = CustomDevotionPlan
        fields = ['familyId', 'members']

    def create(self, validated_data):
        members_data = validated_data.pop('members')
        plan = CustomDevotionPlan.objects.create(**validated_data)
        for member_data in members_data:
            FamilyMember.objects.create(plan=plan, **member_data)
        return plan
    
custom_devotion_plan_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'familyId': openapi.Schema(type=openapi.TYPE_STRING),
        'members': openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'memberId': openapi.Schema(type=openapi.TYPE_STRING),
                    'name': openapi.Schema(type=openapi.TYPE_STRING),
                    'age': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'interests': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_STRING)
                    ),
                    'spiritualMaturityLevel': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        )
    }
)


class MilestoneCelebrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MilestoneCelebration
        fields = ['familyId', 'milestone']

    def validate_milestone(self, value):
        required_fields = ['type', 'date', 'memberName']
        for field in required_fields:
            if field not in value:
                raise serializers.ValidationError(f"{field} is required")
        return value

milestone_celebration_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'familyId': openapi.Schema(type=openapi.TYPE_STRING),
        'milestone': openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'type': openapi.Schema(type=openapi.TYPE_STRING),
                'date': openapi.Schema(type=openapi.TYPE_STRING, format='date'),
                'memberName': openapi.Schema(type=openapi.TYPE_STRING)
            },
            required=['type', 'date', 'memberName']
        )
    },
    required=['familyId', 'milestone']
)


class PrayerRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrayerRequest
        fields = ['familyId', 'requestDetails']

    def validate_requestDetails(self, value):
        required_fields = ['request', 'date']
        for field in required_fields:
            if field not in value:
                raise serializers.ValidationError(f"{field} is required")
        return value
    
prayer_request_schema = openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'familyId': openapi.Schema(type=openapi.TYPE_STRING),
                'requestDetails': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'request': openapi.Schema(type=openapi.TYPE_STRING),
                        'date': openapi.Schema(type=openapi.TYPE_STRING, format='date')
                    },
                    required=['request', 'date']
                )
            },
            required=['familyId', 'requestDetails']
        )
        
class FamilyChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FamilyChallenge
        fields = '__all__'
        

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'
        
feedback_schema = openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'familyId': openapi.Schema(type=openapi.TYPE_STRING),
                'feedback': openapi.Schema(type=openapi.TYPE_STRING)
            },
            required=['familyId', 'feedback']
        )