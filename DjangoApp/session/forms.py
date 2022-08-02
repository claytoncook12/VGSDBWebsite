from django import forms
from django.forms import ModelForm

from .models import Session

class DateInput(forms.DateInput):
    input_type = 'date'

class YoutubeUrlInput(forms.URLInput):
    # Inital Values Not Working
    label ="Youtube URL with embed within"
    initial = 'https://www.youtube.com/embed/{replace with reference}'

class SessionForm(ModelForm):
    class Meta:
        model = Session
        fields = '__all__'
        widgets = {'date' : DateInput(), 'youtube_url': YoutubeUrlInput()}