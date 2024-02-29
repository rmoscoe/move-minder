from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
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

    def form_valid(self, form):
        # If the form is valid, save the user and redirect to the success URL
        return super().form_valid(form)

    def form_invalid(self, form):
        # If the form is invalid, reload the form template in an invalid/error state
        return self.render_to_response(self.get_context_data(form=form))

    class Meta:
        model = User
        fields = ["username", "password1", "password2", "first_name", "last_name", "email", "phone"]

    def clean(self):
        cleaned_data = super().clean()
        print("Cleaning data")
        return cleaned_data