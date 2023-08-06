from django import forms


class InputForm(forms.Form):
    input = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'autofocus': 'autofocus'}),
        max_length=160, initial=''
    )


class DialForm(forms.Form):
    user_type = forms.CharField(
        widget=forms.Select(choices=(('', 'Select User Type'), ('200', 'Eligible'), ('423', 'Already has a loan'), ('404', 'Subscriber NOT Eligible')), attrs={'class': 'form-control', 'id': 'user_type'}),
        max_length=16, initial='', required=False
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'autofocus': 'autofocus'}),
        max_length=160, initial=''
    )
    language = forms.CharField(
        widget=forms.Select(choices=(('sw', 'sw'), ('en', 'en')), attrs={'class': 'form-control'}),
        max_length=16, initial='en'
    )
    service_url = forms.URLField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
