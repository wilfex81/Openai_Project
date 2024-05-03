from django.db import models

class ConflictResolutionAdvice(models.Model):
    keyword = models.CharField(max_length=100)
    advice = models.TextField()

    def __str__(self):
        return self.keyword

class CustomDevotionPlan(models.Model):
    familyId = models.CharField(max_length=100, unique=True)

class FamilyMember(models.Model):
    plan = models.ForeignKey(CustomDevotionPlan, related_name='members', on_delete=models.CASCADE)
    memberId = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    interests = models.JSONField(default=list)
    spiritualMaturityLevel = models.CharField(max_length=100, choices=[
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced')
    ])

    class Meta:
        unique_together = ('plan', 'memberId')
        
class MilestoneCelebration(models.Model):
    familyId = models.CharField(max_length=100)
    milestone = models.JSONField()

    def __str__(self):
        return f"Milestone Celebration for Family: {self.familyId}"

class PrayerRequest(models.Model):
    familyId = models.CharField(max_length=100)
    requestDetails = models.JSONField()

    def __str__(self):
        return f"Prayer Request for Family: {self.familyId}"

    
class FamilyChallenge(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100)

class Feedback(models.Model):
    family_id = models.CharField(max_length=100)
    feedback = models.TextField()

    def __str__(self):
        return f"Feedback from {self.family_id}"

