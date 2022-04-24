from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import (AuthenticationForm, PasswordChangeForm,
                                       UserCreationForm)
from django.shortcuts import redirect, render


def signup(request):
    context = {}
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = request.user
            if user is not None:
                return redirect('login')
            else:
                print('user is none')
        else:
            form = UserCreationForm()
            context['form'] = form
            return render(request, 'users/signup.html', context)
        # context['form'] = form
    if request.method == 'GET':
        form = UserCreationForm()
        context['form'] = form
        return render(request, 'users/signup.html', context)
