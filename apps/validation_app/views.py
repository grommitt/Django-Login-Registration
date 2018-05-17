from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Membership

# Create your views here.
def index(request):
    context = {'all_memberships': Membership.objects.all()}
    return render(request, 'validation_app/index.html', context)

def create(request):
    if request.method == "POST":
    # 1. Call the manager function
        result = Membership.objects.validate_membership(request.POST)

        # 5. Check if errors exist, if they do, add them to messages
        if 'errors' in result:
            for key,value in result['errors'].items():
                messages.error(request, value)
        else:
            messages.success(request, 'YOU CREATED A MEMBERSHIP!')
        return redirect('/')