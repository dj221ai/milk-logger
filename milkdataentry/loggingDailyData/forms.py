from django import forms
from .models import EntryData, RatePerLitre


class EntryDataForm(forms.ModelForm):
    class Meta:
        model = EntryData
        fields = ('date', 'daily_intake', 'extra_intake')

    # def clean(self):
    #     if self.is_valid():
    #         date = self.cleaned_data['date']
    #         daily_intake = self.cleaned_data['daily_intake']
    #         extra_intake = self.cleaned_data['extra_intake']


class RateForm(forms.Form):
    rate_per_litre = forms.FloatField(label='rate of milk', widget=forms.NumberInput(
        attrs={
            'id': 'number_field',
            'step': 'any',
        }
    ))

