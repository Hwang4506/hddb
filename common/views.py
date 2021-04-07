from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from common.forms import UserForm


def signup(request):
    """
    계정생성
    """
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('common:signupsuccess')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})

def signupsuccess(request):
    """
        계정생성 성공
                   """
    return render(request, 'common/signupsuccess.html')