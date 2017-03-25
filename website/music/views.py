from django.http import HttpResponse

def index(request):
    return HttpResponse('<h1>Music App Home</h1>')