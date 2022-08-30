from django import forms
from django.forms import ModelForm

from .models import Session, PlayedTuneGroup

from .session_shared_functions import check_youtube_url

class DateInput(forms.DateInput):
    input_type = 'date'

class SessionForm(ModelForm):
    class Meta:
        model = Session
        fields = '__all__'
        widgets = {'date' : DateInput()}

    # Additional Checks for SessionForm
    def clean(self):
        # Call clean() method to ensure base class validation
        super(SessionForm, self).clean()
        
        # Get Field Value from cleaned_data dict
        youtube_url_value = self.cleaned_data.get('youtube_url','')

        # additional check for youtube_url
        valid, message = check_youtube_url(youtube_url_value)
        if not valid:
            message = message
            self.add_error('youtube_url', message)

class PlayedTuneGroupForm(ModelForm):
    class Meta:
        model = PlayedTuneGroup
        fields = "__all__"
