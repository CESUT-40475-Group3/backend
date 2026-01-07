from django.contrib import admin

from user_profile.models import UserProfile, Skill, Education, WorkExperience

admin.site.register(UserProfile)
admin.site.register(Skill)
admin.site.register(Education)
admin.site.register(WorkExperience)
