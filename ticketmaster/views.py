from django.shortcuts import render
import requests
from .models import Ticket


def view_home(request):
    response = requests.get('https://randomuser.me/api/')
  #  print(response.json())

    return render(request, 'ticketMasterKnockOff.html')

