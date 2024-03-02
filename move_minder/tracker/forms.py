from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
import json
from .models import Parcel, UserProfile
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
        print(json.dumps(cleaned_data))
        return cleaned_data

    def is_valid(self):
        valid = super().is_valid()
        print(f"Valid: {valid}")
        if not valid:
            # If the form is not valid, manually handle form-wide errors
            # and add them to the form's non_field_errors attribute
            errors = self._errors.setdefault(forms.forms.NON_FIELD_ERRORS, forms.utils.ErrorList())
            for field, field_errors in self.errors.items():
                if field != '__all__':
                    continue
                for error in field_errors:
                    errors.append(error)
        return valid