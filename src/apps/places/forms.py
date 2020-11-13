from django import forms
from .models import Memory


class MemoryModelForm(forms.ModelForm):
    class Meta:
        model = Memory
        fields = ('title', 'description', 'lat', 'lon', 'zoom')
        widgets = {'lat': forms.HiddenInput(),
                   'lon': forms.HiddenInput(),
                   'zoom': forms.HiddenInput()}
