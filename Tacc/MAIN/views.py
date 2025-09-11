from django.shortcuts import render, redirect, HttpResponse
from .models import Release

def landing_page(request):
    """
    Widok strony głównej (landing page).
    """
    if request.user.is_authenticated:
        # Jeśli użytkownik jest zalogowany, przekieruj do modułu /accountancy
        return redirect('/accountancy')

    return render(request, 'MAIN/landing_page.html')


def get_list_of_versions(request):
    releases = Release.objects.all().order_by('-release_date')
    return render(request, 'Accountancy/versions.html.jinja', {'versions': releases})

def get_icons(request):
    return HttpResponse(open('static/icons.svg').read(), content_type='image/svg+xml')