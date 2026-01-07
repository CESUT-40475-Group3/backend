from django.db import models

from core.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.user.username


class Skill(models.Model):
    user_profile = models.ForeignKey(UserProfile, related_name='skills', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    proficiency_level = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.proficiency_level})"


class Education(models.Model):
    user_profile = models.ForeignKey(UserProfile, related_name='educations', on_delete=models.CASCADE)
    institution = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    field_of_study = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.degree} at {self.institution}"


class WorkExperience(models.Model):
    user_profile = models.ForeignKey(UserProfile, related_name='work_experiences', on_delete=models.CASCADE)
    company = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    responsibilities = models.TextField()

    def __str__(self):
        return f"{self.position} at {self.company}"
