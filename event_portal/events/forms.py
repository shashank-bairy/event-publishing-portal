from django import forms
from django.contrib.auth.models import User
from .models import Event

class EventForm(forms.ModelForm):
    name = forms.CharField(max_length=100)
    thumbnail = forms.ImageField()
    description = forms.CharField(widget=forms.Textarea(attrs={"rows": 7, "cols": 20}))
    date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    time = forms.TimeField(widget=forms.TextInput(attrs={'type': 'time'}))
    venue = forms.CharField(max_length=100)
    address = forms.CharField(max_length=250)
    
    class Meta:
        model = Event 
        fields = ['name', 'thumbnail', 'description', 'date', 'time', 'venue', 'address']

