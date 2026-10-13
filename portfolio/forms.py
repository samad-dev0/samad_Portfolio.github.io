from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ValidationError

from .models import ContactMessage

User = get_user_model()


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

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user and user.is_authenticated:
            full_name = user.get_full_name() or user.username
            if not self.initial.get("name"):
                self.initial["name"] = full_name
            if not self.initial.get("email"):
                self.initial["email"] = user.email


class LoginForm(forms.Form):
    username_or_email = forms.CharField(
        label="Adresse e-mail ou nom d’utilisateur",
        widget=forms.TextInput(
            attrs={
                "class": "auth_input",
                "placeholder": "Ex : nom@exemple.com",
                "autocomplete": "username",
                "required": True,
            }
        ),
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(
            attrs={
                "class": "auth_input",
                "placeholder": "Entrez votre mot de passe",
                "autocomplete": "current-password",
                "required": True,
            }
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        identifier = (cleaned_data.get("username_or_email") or "").strip()
        password = cleaned_data.get("password")

        if identifier and password:
            user = None
            if "@" in identifier:
                matching_user = User.objects.filter(email__iexact=identifier).first()
                if matching_user:
                    user = authenticate(username=matching_user.username, password=password)
            if not user:
                user = authenticate(username=identifier, password=password)

            if not user:
                raise ValidationError("Adresse e-mail / nom d’utilisateur ou mot de passe incorrect.")
            if not user.is_active:
                raise ValidationError("Ce compte est désactivé.")

            cleaned_data["user"] = user

        return cleaned_data


class RegisterForm(forms.Form):
    name = forms.CharField(
        max_length=150,
        label="Nom complet",
        widget=forms.TextInput(
            attrs={
                "class": "auth_input",
                "placeholder": "Ex : Alex Dupont",
                "autocomplete": "name",
                "required": True,
            }
        ),
    )
    email = forms.EmailField(
        label="Adresse e-mail",
        widget=forms.EmailInput(
            attrs={
                "class": "auth_input",
                "placeholder": "Ex : alex@exemple.com",
                "autocomplete": "email",
                "required": True,
            }
        ),
    )
    password = forms.CharField(
        min_length=6,
        label="Mot de passe",
        widget=forms.PasswordInput(
            attrs={
                "class": "auth_input",
                "placeholder": "6 caractères minimum",
                "autocomplete": "new-password",
                "required": True,
            }
        ),
    )
    password_confirm = forms.CharField(
        label="Confirmation du mot de passe",
        widget=forms.PasswordInput(
            attrs={
                "class": "auth_input",
                "placeholder": "Répétez le mot de passe",
                "autocomplete": "new-password",
                "required": True,
            }
        ),
    )

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("Un compte avec cette adresse e-mail existe déjà. Veuillez vous connecter.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error("password_confirm", "Les deux mots de passe ne correspondent pas.")

        return cleaned_data

    def save(self):
        name = self.cleaned_data["name"].strip()
        email = self.cleaned_data["email"].strip().lower()
        password = self.cleaned_data["password"]

        base_username = email.split("@")[0].replace(".", "_")[:25]
        username = base_username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}_{counter}"
            counter += 1

        name_parts = name.split(" ", 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ""

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        return user
