from django.contrib import admin
from .models import (ConflictResolutionAdvice, CustomDevotionPlan, FamilyChallenge, FamilyMember,
                    Feedback, MilestoneCelebration, PrayerRequest)

admin.site.register(ConflictResolutionAdvice)
admin.site.register(CustomDevotionPlan)
admin.site.register(FamilyChallenge)
admin.site.register(FamilyMember)
admin.site.register(Feedback)
admin.site.register(MilestoneCelebration)
admin.site.register(PrayerRequest)
