from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
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
    phone = PhoneNumberField()

    class Meta:
        model = User
        fields = ["username", "password1", "password2", "first_name", "last_name", "email", "phone"]

class MoveForm(ModelForm):
    class Meta:
        model = Move
        field_groups = [
            ("Properties", ["nickname", "primary_user", "secondary_users", "start_date", "end_date"]),
            ("Origin", ["origin_address1", "origin_address2", "origin_city", "origin_state_province", "origin_postal_code", "origin_country"]),
            ("Destination", ["destination_address1", "destination_address2", "destination_city", "destination_state_province", "destination_postal_code", "destination_country"])
        ]

        def __iter__(self):
            for group_name, field_names in self.field_groups:
                field_groups = []
                for field_name in field_names:
                    field_groups.append(self[field_name])
                yield group_name, field_groups

class ParcelForm(ModelForm):
    class Meta:
        model = Parcel
        fields = ["move_id", "type", "room", "contents", "photo", "weight", "status"]