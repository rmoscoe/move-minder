from django.contrib.auth.models import User
from django.db import models
from django.db.models import Model
from phonenumber_field.modelfields import PhoneNumberField
from .utils import validate_postal_code

# Create your models here.
state_or_province_to_abbrev = {
    "AL": "Alabama",
    "AK": "Alaska",
    "AB": "Alberta",
    "AZ": "Arizona",
    "AR": "Arkansas",
    "BC": "British Columbia",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DE": "Delaware",
    "FL": "Florida",
    "GA": "Georgia",
    "HI": "Hawaii",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "IA": "Iowa",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "ME": "Maine",
    "MB": "Manitoba",
    "MD": "Maryland",
    "MA": "Massachusetts",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MS": "Mississippi",
    "MO": "Missouri",
    "MT": "Montana",
    "NE": "Nebraska",
    "NV": "Nevada",
    "NB": "New Brunswick",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NY": "New York",
    "NL": "Newfoundland and Labrador",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "NT": "Northwest Territories",
    "NS": "Nova Scotia",
    "NU": "Nunavut",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "ON": "Ontario",
    "OR": "Oregon",
    "PA": "Pennsylvania",
    "PE": "Prince Edward Island",
    "QC": "Quebec",
    "RI": "Rhode Island",
    "SK": "Saskatchewan",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VT": "Vermont",
    "VA": "Virginia",
    "WA": "Washington",
    "WV": "West Virginia",
    "WI": "Wisconsin",
    "WY": "Wyoming",
    "YT": "Yukon Territory",
    "DC": "District of Columbia",
    "AS": "American Samoa",
    "GU": "Guam",
    "MP": "Northern Mariana Islands",
    "PR": "Puerto Rico",
    "UM": "United States Minor Outlying Islands",
    "VI": "U.S. Virgin Islands"
}

class UserProfile(Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = PhoneNumberField()
    recent_pages = models.JSONField(blank=True, default=list)
    created = models.DateTimeField(auto_now_add=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True, blank=True)


class Move(Model):
    nickname = models.CharField(max_length=80)
    primary_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    secondary_users = models.ManyToManyField(User, verbose_name="Add Users", related_name='moves_as_secondary', null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    origin_address1 = models.CharField("Address 1", max_length=80)
    origin_address2 = models.CharField("Address 2", max_length=80, null=True, blank=True)
    origin_city = models.CharField("City", max_length=80)
    origin_state_province = models.CharField("State/Province", max_length=2, choices=state_or_province_to_abbrev)
    origin_postal_code = models.CharField("Zip/Postal Code", max_length=7, validators=[validate_postal_code])
    origin_country = models.CharField("Country", max_length=40, choices={"Canada": "Canada", "USA": "USA"})
    destination_address1 = models.CharField("Address 1", max_length=80)
    destination_address2 = models.CharField("Address 2", max_length=80, null=True, blank=True)
    destination_city = models.CharField("City", max_length=80)
    destination_state_province = models.CharField("State/Province", max_length=2, choices=state_or_province_to_abbrev)
    destination_postal_code = models.CharField("Zip/Postal Code", max_length=7, validators=[validate_postal_code])
    destination_country = models.CharField("Country", max_length=40, choices={"Canada": "Canada", "USA": "USA"})
    created = models.DateTimeField(auto_now_add=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True, blank=True)

    @staticmethod
    def handle_primary_user_deletion(instance, **kwargs):
        if kwargs['action'] == 'pre_remove' and instance.primary_user_id in kwargs['value']:
            instance.primary_user = instance.secondary_users.first()
            instance.secondary_users.remove(instance.primary_user)
            instance.save()
        else:
            instance.delete()
    
models.signals.m2m_changed.connect(Move.handle_primary_user_deletion, sender=Move.secondary_users.through)

class Parcel(Model):
    type_choices = {
        "Appliance": "Appliance", 
        "Bag": "Bag", 
        "Box": "Box", 
        "Crate": "Crate", 
        "Furniture": "Furniture", 
        "Other": "Other", 
        "Storage Bin": "Storage Bin", 
        "Suitcase": "Suitcase"
    }
    status_choices = ["Packed", "In Transit", "Lost", "Received", "Damaged", "Accepted"]

    move_id = models.ForeignKey(Move, on_delete=models.CASCADE)
    type = models.CharField(max_length=40, choices=type_choices, default="Box")
    room = models.CharField(max_length=40, help_text="In which room does this parcel belong when it reaches the destination?", null=True, blank=True)
    contents = models.TextField(null=True, blank=True, help_text="Optionally, describe the contents of this parcel.")
    photo = models.ImageField(upload_to='images/', max_length=255, null=True, blank=True)
    weight = models.FloatField(blank=True, null=True, help_text="Optionally, enter the weight of the parcel in pounds.")
    status = models.CharField(max_length=12, choices={choice: choice for choice in status_choices}, default="Ready")
    created = models.DateTimeField(auto_now_add=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True, blank=True)