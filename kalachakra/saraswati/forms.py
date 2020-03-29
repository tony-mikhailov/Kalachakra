from django import forms

from .models import Ritual

class RitualForm(forms.Form):
    ritual = forms.ChoiceField(choices = [])

    def __init__(self, *args, **kwargs):
        super(RitualForm, self).__init__(*args, **kwargs)
        self.fields['ritual'].choices = [(x.pk, x.short_name) for x in Ritual.objects.filter(is_hural=True)]
        # self.fields['ritual'].choices = [('1', '111111')]
        # slef.fields['id_for_label']
    