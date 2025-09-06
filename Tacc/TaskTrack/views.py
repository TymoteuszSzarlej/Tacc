from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def dashboard(request):
    """
    Widok dashboardu dla modułu TaskTrack.
    """
    return render(request, 'TaskTrack/dashboard/dashboard.html')