import os
from django.shortcuts import render_to_response

# the basic view for the home page renders templates/home/home.html
def home(request):
    return render_to_response('home/home.html')
