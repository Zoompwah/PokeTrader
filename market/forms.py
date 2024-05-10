from django import forms
from .models import Listing
from collection.models import Card

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['card', 'price']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ListingForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['card'].queryset = Card.objects.filter(collection__user=user)