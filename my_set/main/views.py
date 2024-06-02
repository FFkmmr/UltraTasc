from django.shortcuts import render

def index(request):
    values = {
        'isEntered': False,
        'handler': 'Portfolio handler',
        'user': 'name',
    }
    template_name = 'main/index.html'
    return render(request, template_name, {'values': values})