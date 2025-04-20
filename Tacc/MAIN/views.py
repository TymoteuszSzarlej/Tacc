from django.shortcuts import render, redirect

def landing_page(request):
    """
    Widok strony głównej (landing page).
    """
    if request.user.is_authenticated:
        # Jeśli użytkownik jest zalogowany, przekieruj do modułu /accountancy
        return redirect('/accountancy')

    return render(request, 'MAIN/landing_page.html')
