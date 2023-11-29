from django import forms
from .models import Ticket


class TicketForm(forms.ModelForm):
    search_term = forms.CharField(max_length=50)
    search_city = forms.CharField(max_length=50)
    # form class will generate input for us
    # create instance in view

# class Meta:
#    fields = '__all__'
#    model = Ticket
# This meta class means we might add extra features

# we want this class to generate validation for us
