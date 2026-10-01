from django import forms

from .models import ContactMessage


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["email", "name", "phone", "message"]
        widgets = {
            "email": forms.EmailInput(attrs={"class": "input_field", "placeholder": "Email", "autocomplete": "email"}),
            "name": forms.TextInput(attrs={"class": "input_field", "placeholder": "Nom utilisateur", "autocomplete": "name"}),
            "phone": forms.TelInput(attrs={"class": "input_field", "placeholder": "Téléphone", "autocomplete": "tel"}),
            "message": forms.Textarea(attrs={"class": "input_field", "placeholder": "Message", "rows": 4}),
        }
