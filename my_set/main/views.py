from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CreateUserForm
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q
import json
from django.views.decorators.csrf import csrf_exempt

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


def project_list_view(request):
    projects = Project.objects.all()
    industries = Industry.objects.all()
    technologies = Technology.objects.all()

    context = {
        'projects': projects,
        'industries': industries,
        'technologies': technologies,
    }

    return render(request, 'main/projects.html', context)

@csrf_exempt
def project_filter_view(request):
    selected_industries = request.POST.get('industries')
    selected_technologies = request.POST.get('technologies')
    selected_industries = json.loads(selected_industries) if selected_industries else []
    selected_technologies = json.loads(selected_technologies) if selected_technologies else []
    
    filters = {}

    if selected_industries:
        filters['industries__name__in'] = selected_industries
    if selected_technologies:
        filters['technologies__name__in'] = selected_technologies

    projects = Project.objects.filter(
        **filters
    )

    context = {
        'projects': projects,
    }

    html = render_to_string('main/projects.html', context)
    return JsonResponse({'html': html})
