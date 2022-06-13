from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path("", views.index, name="index"),

    path("projects/<int:id>", views.projects, name="projects"),
    path('submit-project/', views.submit_project,name="submit-project"),




    path('search/', views.search_results, name='search_results'),
    path("accounts/profile/", views.profile_view, name="profile"),


]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) 