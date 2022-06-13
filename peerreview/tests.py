from django.test import TestCase
from django.contrib.auth.models import User
from .models import Category, Projects, Rating, UserProfile


class CategoryTest(TestCase):

    def setUp(self):
        self.html = Category(name='Music')

    def test_instance(self):
        self.assertTrue(isinstance(self.html, Category))

    def test_save(self):
        self.html.save_category()
        categoriess = Category.objects.all()
        self.assertTrue(len(categoriess) > 0)

    def test_delete(self):
        self.html.save_category()
        self.html.delete_category()
        categoriess = Category.objects.all()
        self.assertTrue(len(categoriess) == 0)


class ProjectsTest(TestCase):

    def setUp(self):
        # Creating a new editor and saving it

        self.html = Projects(description='Music')
        self.html.save_project()

        # Creating a new tag and saving it
        self.new_project = Category(name='testing')
        self.new_project.save()

        self.new_project = Projects(description='This is a random test project', image='', category=self.html)
        self.new_project.save()
        self.new_project.category.add(self.new_project)

    def tearDown(self):
        Category.objects.all().delete()
        Projects.objects.all().delete()


class UserProfileTestClass(TestCase):
    # setup method
    def setUp(self):
        self.user_name = User(username='mwangi')
        self.user_name.save()
        self.user_profile = UserProfile(user=self.user_name, image="", bio="bio")

    def tearDown(self):
        User.objects.all().delete()
        UserProfile.objects.all().delete()

    def test_instance(self):
        self.assertTrue(isinstance(self.user_profile, UserProfile))

    def test_save(self):
        self.user_name.save_profile()
        profiles = UserProfile.objects.all()
        self.assertTrue(len(profiles) > 0)

    def test_delete(self):
        self.user_name.save_profile()
        self.user_name.delete_profile()
        profiless = UserProfile.objects.all()
        self.assertTrue(len(profiless) == 0)

    def test_filter_profile_by_id(self):
        id = 1