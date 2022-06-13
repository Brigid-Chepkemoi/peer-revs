from django.shortcuts import render, redirect
from django_registration.backends.one_step.views import RegistrationView
from django.contrib.auth.models import User
from .forms import RateForm, SubmitProjectForm, UserProfileForm
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from .models import Projects, Rating, UserProfile, Category


# Create your views here.


def index(request):
    technology = request.GET.get('technology')
    if technology == None:
        projects = Projects.objects.all()
    else:
        projects = Projects.objects.filter(technologies__name=technology)

    technologies = Category.objects.all()

    context = {'technologies': technologies, 'projects': projects}

    return render(request, 'index.html', context)


# def projects(request, pk):
#     project = Projects.objects.get(id=pk)

#     return render(request, "projects.html",{'project':project})
@login_required(login_url='/accounts/login/')
def projects(request, id):
    user = UserProfile.objects.get(user=request.user)
    project = Projects.objects.get(id=id)

    ratings = Rating.objects.filter(project=project).last()
    tech_tags = project.technologies.split(",")

    try:
        rates = Rating.objects.filter(user=user, project=project).first()
    except Rating.DoesNotExist:
        rates = None

    if rates is None:
        rates_status = False
    else:
        rates_status = True

    form = RateForm()
    rating = None
    if request.method == 'POST':
        form = RateForm(request.POST)
        if form.is_valid():
            rate = form.save(commit=False)
            rate.user = user
            rate.project = project
            rate.save()
        try:
            rating = Rating.objects.filter(project_id=id)
        except Rating.DoesNotExist:
            rating = None
        design = form.cleaned_data['design']
        usability = form.cleaned_data['usability']
        content = form.cleaned_data['content']
        rate.average = (design + usability + content) / 2
        rate.save()

        design_ratings = [d.design for d in rating]
        design_average = sum(design_ratings) / len(design_ratings)

        usability_ratings = [us.usability for us in rating]
        usability_average = sum(usability_ratings) / len(usability_ratings)

        content_ratings = [content.content for content in rating]
        content_average = sum(content_ratings) / len(content_ratings)
        score = (design_average + usability_average + content_average) / 3

        rate.design_average = round(design_average, 2)
        rate.usability_average = round(usability_average, 2)
        rate.content_average = round(content_average, 2)
        rate.score = round(score, 2)

        rate.save()
        return redirect("projects", id=project.id)
    else:
        form = RateForm()

    ctx = {
        "project": project,
        "ratings": ratings,
        "form": form,
        "tech_tags": tech_tags,
        "rates_status": rates_status
    }
    return render(request, "projects.html", ctx)


@login_required(login_url='/accounts/login/')
def user_profile(request, username):
    current_user = request.user
    user_selected = User.objects.get(username=username)
    user_profile = User.filter_profile_by_id(user_selected.id)
    projects = Projects.objects.filter(user=user_profile)
    if request.user == user_selected:
        return redirect('profile', username=username)

    ctx = {
        "user_profile": user_profile,
        "projects": projects,

    }
    return render(request, 'profile.html', ctx)


@login_required(login_url='/accounts/login/')
def profile_view(request):
    user_logged = request.user
    user = UserProfile.objects.get(user=user_logged)
    form = UserProfileForm()

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        # print('the.....',request.POST['user_name'])

        if form.is_valid():
            user = form.save(commit=False)
            # print('hello.....',form)
            user.save()
            return redirect('profile')

    ctx = {
        "user_logged": user_logged,
        "user": user,
        "form": form,
    }
    return render(request, 'profile.html', ctx)


@login_required(login_url='/accounts/login/')
def logout(request):
    logout(request)
    return redirect('login')


@login_required(login_url='/accounts/login/')
def submit_project(request):
    current_user = request.user
    user = UserProfile.objects.get(user=current_user)
    form = SubmitProjectForm()
    if request.method == 'POST':
        form = SubmitProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = user
            project.save()
            return redirect('/')
    else:
        form = SubmitProjectForm()
    ctx = {
        'form': form
    }

    return render(request, "submit-project.html", ctx)

@login_required(login_url='login')
def search_results(request):
    if request.GET['search_projects'] and 'search_projects' in request.GET:
        name = request.GET.get("search_projects")
        results = UserProfile.search_projects(name)
        for r in results:
            print(r.user)
        message = f'{name}'
        params = {
            'results': results,
            'message': message,
            'name': name,

        }
        return render(request, 'peerreviews/search.html', params)
    else:
        message = "You haven't searched for any user"
    return render(request, 'peerreviews/search.html', {'message': message})