from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def register(request):
    return render(request, 'profiles/register.html', context={'extra_title': 'Register'})


@login_required()
def profile(request):
    return render(request, 'profiles/profile.html', context={'extra_title': 'Profile'})


@login_required()
def edit_profile(request):
    return render(request, 'profiles/edit_profile.html', context={'extra_title': 'Edit profile'})
