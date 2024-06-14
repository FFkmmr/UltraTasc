from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CreateUserForm

from .models import Project, Technology, Industry

@login_required(login_url='login')
def index(request):
    technologies = Technology.objects.all()
    industries = Industry.objects.all()
    context = {
        'technologies': technologies,
        'industries': industries,
    }
    return render(request, 'main/index.html', context)
def register_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                return redirect('login')
            
        context = {'form': form}
        return render(request, 'main/register.html', context)
def login_page(request):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else: 
                messages.info(request, 'Username OR password is incorrect.')
        context = {}
        return render(request, 'main/login.html', context)
def logout_user(request):
    logout(request)
    return redirect('login')

from django.db.models import Q

def project_list(request):
    selected_industries = request.GET.getlist('industries[]')
    selected_technologies = request.GET.getlist('technologies[]')
    projects = Project.objects.all()

    if selected_industries:
        projects = projects.filter(industries__name__in=selected_industries).distinct()
    if selected_technologies:
        projects = projects.filter(technologies__name__in=selected_technologies).distinct()

    if selected_industries:
        for industry in selected_industries:
            projects = projects.exclude(~Q(industries__name=industry))
    if selected_technologies:
        for technology in selected_technologies:
            projects = projects.exclude(~Q(technologies__name=technology))

    industries = Industry.objects.all()
    technologies = Technology.objects.all()

    context = {
        'industries': industries,
        'technologies': technologies,
        'projects': projects,
    }
    
    return render(request, 'main/projects.html', context)