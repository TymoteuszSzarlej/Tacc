from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from . import forms
from MAIN.utils import log
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import CustomUserCreationForm 

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        log(f"przeslano formularz rejestracji użytkownika\t{form}", 'inf')

        if form.is_valid():
            log('formularz poprawny', 'suc')

            user = form.save(commit=False)
            user.email = form.cleaned_data.get('email')
            user.save()

            return redirect('login')

        else:
            log('formularz niepoprawny', 'err')
            print(form.errors)

            if form.cleaned_data.get('password1') != form.cleaned_data.get('password2'):
                messages.error(request, "Hasła nie są zgodne.")
            elif User.objects.filter(username=request.POST.get('username')).exists():
                messages.error(request, "Nazwa użytkownika jest już zajęta.")
            elif User.objects.filter(email=request.POST.get('email')).exists():
                messages.error(request, "Adres e-mail jest już zajęty.")
            else:
                messages.error(request, "Wystąpił błąd podczas rejestracji. Sprawdź poprawność danych.")

        log(
                f"username\t{request.POST.get('username')}\n"
                f"email\t{request.POST.get('email')}\n"
                f"password1\t{request.POST.get('password1')}\n"
                f"password2\t{request.POST.get('password2')}",
                'deb'
            )
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html.jinja', {'form': form})
