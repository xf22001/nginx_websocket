from django.shortcuts import render

# Create your views here.
import logging

logger = logging.getLogger('django.request')

# Create your views here.
def index(request):
    return render(request, 'index.html')
