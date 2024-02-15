from django.forms import ModelForm
from .models import Parcel

class ParcelStatusForm(ModelForm):
    class Meta:
        model = Parcel
        fields = ["status"]