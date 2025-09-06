from django.shortcuts import render
from django.http import JsonResponse
import uuid


sessions = {}


def welcomeF(request):
    """DONE"""

    return render(request, "game.html", {})

