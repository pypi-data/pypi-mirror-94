from django import forms


class PhoneForm(forms.Form):
    phone = forms.CharField(max_length=32, label='Номер телефона')


class PassCodeForm(forms.Form):
    pass_code = forms.CharField(max_length=4, label='Код')
