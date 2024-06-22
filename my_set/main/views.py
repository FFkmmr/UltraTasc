from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from .models import Project, Technology, Industry
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from .forms import CreateUserForm, CreateProjectForm
from django.db import transaction
import json
import csv

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
@login_required(login_url='login')
def index(request):
    technologies = Technology.objects.all()
    industries = Industry.objects.all()
    projects = Project.objects.all()
    context = {
        'technologies': technologies,
        'industries': industries,
        'projects' : projects,
    }
    return render(request, 'main/index.html', context)
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
@login_required(login_url='login')
def import_csv_view(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        fs = FileSystemStorage()
        filename = fs.save(csv_file.name, csv_file)
        file_path = fs.path(filename)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                with transaction.atomic():
                    for row in reader:
                        project = Project(
                            title=row['title'],
                            url=row['url'],
                            description=row['description'].strip()
                        )
                        project.save()
                        
                        tech_names = row['technologies'].split(',')
                        industry_names = row['industries'].split(',')
                        
                        technologies = []
                        for tech_name in tech_names:
                            technology, created = Technology.objects.get_or_create(name=tech_name.strip())
                            technologies.append(technology)
                        
                        industries = []
                        for industry_name in industry_names:
                            industry, created = Industry.objects.get_or_create(name=industry_name.strip())
                            industries.append(industry)
                        
                        project.technologies.set(technologies)
                        project.industries.set(industries)
            
            return redirect('home')
        
        except Exception as e:
            return HttpResponse(f"Error: {e}")
    
    return render(request, 'import_csv.html')


def add_project(request):
    if request.method == 'POST':
        form = CreateProjectForm(request.POST)
        if form.is_valid():
            project = form.save()

            new_technologies = form.cleaned_data.get('new_technologies')
            if new_technologies:
                tech_list = [tech.strip() for tech in new_technologies.split(',')]
                for tech_name in tech_list:
                    technology, created = Technology.objects.get_or_create(name=tech_name)
                    project.technologies.add(technology)
            new_industries = form.cleaned_data.get('new_industries')
            if new_industries:
                ind_list = [ind.strip() for ind in new_industries.split(',')]
                for ind_name in ind_list:
                    industry, created = Industry.objects.get_or_create(name=ind_name)
                    project.industries.add(industry)

            return redirect('home')
    else:
        form = CreateProjectForm()
    return render(request, 'add_project.html', {'form': form})