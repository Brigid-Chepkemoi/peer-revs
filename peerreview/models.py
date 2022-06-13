from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    technologies = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name

    def save_category(self):
        self.save()

    def delete_category(self):
        self.delete()

    class Meta:
        ordering = ['name']


class UserProfile(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # user=models.OneToOneField(User, on_delete=models.CASCADE)
    image = CloudinaryField('image')

    user_name = models.CharField(max_length=300, null=True)
    bio = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return str(self.user_name)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, created, **kwargs):
        instance.userprofile.save()

    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()


class Projects(models.Model):
    image = CloudinaryField('image')
    description = models.TextField()
    name = models.TextField()
    link = models.URLField()
    technologies = models.CharField(max_length=200, blank=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='posts')
    posted_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ["pk"]

    def save_project(self):
        self.save()

    def delete_project(self):
        self.delete()

    @classmethod
    def get_project_by_id(cls, id):
        project = Projects.objects.filter(id=id)
        return project

    def __str__(self):
        return self.description

    def save_projects(self):
        self.save()

    def delete_projects(self):
        self.delete()

    @classmethod
    def search_by_name(cls, search_term):
        projectss = cls.objects.filter(name__icontains=search_term)
        return projectss


class Rating(models.Model):
    rating = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
    )

    design = models.IntegerField(choices=rating, default=0, blank=True)
    usability = models.IntegerField(choices=rating, blank=True)
    content = models.IntegerField(choices=rating, blank=True)
    score = models.FloatField(default=0, blank=True)
    design_average = models.FloatField(default=0, blank=True)
    usability_average = models.FloatField(default=0, blank=True)
    content_average = models.FloatField(default=0, blank=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, related_name='rater')
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, related_name='ratings', null=True)
    rated_at = models.DateTimeField(auto_now_add=True)

    def save_rating(self):
        self.save()

    def delete_rating(self):
        self.delete()

    @classmethod
    def get_project_rating(cls, pk):
        rating = Rating.objects.filter(project_id=pk).all()
        return rating

    def __str__(self):
        return f'{self.project} Rating'
