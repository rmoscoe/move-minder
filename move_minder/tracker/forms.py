from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm
import json
from .models import Parcel, UserProfile, Move
from phonenumber_field.formfields import PhoneNumberField

class ParcelStatusForm(ModelForm):
    class Meta:
        model = Parcel
        fields = ["status"]

class SignUpForm(UserCreationForm):
    phone = PhoneNumberField()
    first_name = forms.CharField(max_length=40, required=True)
    last_name = forms.CharField(max_length=40, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "password1", "password2", "first_name", "last_name", "email", "phone"]

    def clean(self):
        cleaned_data = super(ModelForm, self).clean()
        return cleaned_data

    def is_valid(self):
        valid = super().is_valid()
        print(f"Valid: {valid}")
        if not valid:
            errors = self._errors.setdefault(forms.forms.NON_FIELD_ERRORS, forms.utils.ErrorList())
            for field, field_errors in self.errors.items():
                if field != '__all__':
                    continue
                for error in field_errors:
                    errors.append(error)
        return valid

class UpdateUserForm(ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput, required=False)
    phone = PhoneNumberField()

    class Meta:
        model = User
        fields = ["username", "password1", "password2", "first_name", "last_name", "email", "phone"]

        def __init__(self, *args, **kwargs):
            self.user = kwargs.get("instance", None)
            super().__init__(*args, **kwargs)

            self.fields["username"].initial = self.user.username
            self.fields["first_name"].initial = self.user.first_name
            self.fields["last_name"].initial = self.user.last_name
            self.fields["email"].initial = self.user.email

        def clean_password2(self):
            password1 = self.cleaned_data.get("password1")
            password2 = self.cleaned_data.get("password2")
            if password1 and password2 and password1 != password2:
                raise ValidationError("Passwords don't match")
            return password2

class MoveForm(ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))

    class Meta:
        model = Move
        fields = ["nickname", "primary_user", "secondary_users", "start_date", "end_date", "origin_address1", "origin_address2", "origin_city", "origin_state_province", "origin_postal_code", "origin_country", "destination_address1", "destination_address2", "destination_city", "destination_state_province", "destination_postal_code", "destination_country"]

        def __init__(self, *args, request=None, **kwargs):
            self.user = kwargs.get("instance", None)
            super().__init__(*args, **kwargs)
            self.request = request

            if request is not None and request.resolver_match.url_name == "move-update":
                instance = kwargs.get("instance")
                for field in self.fields.keys():
                    self.field[field].initial = instance[field]

class ParcelForm(ModelForm):
    class Meta:
        model = Parcel
        fields = ["move_id", "type", "room", "contents", "photo", "weight", "status"]
    
        def __init__(self, *args, request=None, **kwargs):
            self.user = kwargs.get("instance", None)
            super().__init__(*args, **kwargs)
            self.request = request

            if request is not None and request.resolver_match.url_name == "parcel-update":
                instance = kwargs.get("instance")
                for field in self.fields.keys():
                    self.field[field].initial = instance[field]