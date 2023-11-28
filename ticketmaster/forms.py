from django import forms
from .models import Ticket


class TicketForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = Ticket
        # This meta class means we might add extra features