from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Move, Parcel
from phonenumber_field.formfields import PhoneNumberField

class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=40)
    last_name = forms.CharField(max_length=40)
    phone = PhoneNumberField()
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "password1", "password2", "first_name", "last_name", "email", "phone"]

class MoveForm(ModelForm):
    class Meta:
        model = Move
        fields = ["nickname", "secondary_users", "start_date", "end_date", "origin_address1", "origin_address2", "origin_city", "origin_state_province", "origin_postal_code", "origin_country", "destination_address1", "destination_address2", "destination_city", "destination_state_province", "destination_postal_code", "destination_country"]

class CreateParcelForm(ModelForm):
    class Meta:
        model = Parcel
        fields = ["type", "room", "contents", "photo", "weight"]

class ParcelStatusForm(ModelForm):
    class Meta:
        model = Parcel
        fields = ["status"]

class UpdateParcelForm(ModelForm):
    class Meta:
        model = Parcel
        fields = ["type", "room", "contents", "photo", "weight", "status"]