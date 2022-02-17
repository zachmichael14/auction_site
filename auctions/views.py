from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    
    context = {
        "popular": ["g", "d" "d", "d"]

    }
    return render(request, 'auctions/index.html', context)


     