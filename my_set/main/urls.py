from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('project_list/', views.project_filter_view, name='project_list'),
    path('register/', views.register_page, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('import_csv/', views.import_csv_view, name='import_csv'),
    path('add-project/', views.add_project, name="add_project"),
] 