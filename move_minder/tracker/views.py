from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.base import TemplateView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import ParcelStatusForm
from .models import Move, Parcel
from phonenumber_field.formfields import PhoneNumberField

# Create your views here.
class HomePageView(TemplateView):
    template_name = "home.html"

    """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # add additional context as necessary
        return context
    """

class SignupView(CreateView):
    model = User
    template_name = "signup.html"
    first_name = forms.CharField(max_length=40)
    last_name = forms.CharField(max_length=40)
    phone = PhoneNumberField()
    email = forms.EmailField()
    success_url = reverse_lazy('sign-up')
    fields = ["username", "password1", "password2", "first_name", "last_name", "email", "phone"]

class DashboardView(TemplateView, LoginRequiredMixin):
    template_name = "dashboard.html"
    login_url = reverse_lazy("login")

class UserListView(ListView, LoginRequiredMixin):
    model = User
    paginate_by = 50
    login_url = reverse_lazy("login")
    context_object_name = "users"

class UserDetailView(DetailView, LoginRequiredMixin):
    model = User

class MoveListView(ListView, LoginRequiredMixin):
    paginate_by = 10
    context_object_name = "moves"

    def get_queryset(self):
        user_id = self.request.user.id
        return Move.objects.filter(Q(primary_user=user_id) | Q(secondary_users__contains=user_id))

class MoveDetailView(DetailView, LoginRequiredMixin):
    model = Move

    def get_context_data(self, **kwargs):
        # path_list = self.request.path.split("/")
        # move_id = path_list[2]
        move_id = get_object_or_404(Move, pk=self.kwargs["pk"])

        context = super().get_context_data(**kwargs)
        context["parcels"] = Parcel.objects.filter(move_id=move_id)

        return context

class MoveCreateView(CreateView, LoginRequiredMixin):
    model = Move
    fields = ["nickname", "secondary_users", "start_date", "end_date", "origin_address1", "origin_address2", "origin_city", "origin_state_province", "origin_postal_code", "origin_country", "destination_address1", "destination_address2", "destination_city", "destination_state_province", "destination_postal_code", "destination_country"]

class MoveUpdateView(UpdateView, LoginRequiredMixin):
    model = Move
    fields = ["nickname", "secondary_users", "start_date", "end_date", "origin_address1", "origin_address2", "origin_city", "origin_state_province", "origin_postal_code", "origin_country", "destination_address1", "destination_address2", "destination_city", "destination_state_province", "destination_postal_code", "destination_country"]

class MoveDeleteView(DeleteView, LoginRequiredMixin):
    model = Move
    success_url = reverse_lazy("moves-list")

class ParcelDetailView(DetailView, LoginRequiredMixin):
    model = Parcel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ParcelStatusForm()
        return context

class ParcelCreateView(CreateView, LoginRequiredMixin):
    model = Parcel
    fields = ["type", "room", "contents", "photo", "weight"]

class ParcelStatusUpdateView(SingleObjectMixin, FormView, LoginRequiredMixin):
    template_name = "parcel_detail.html"
    form_class = ParcelStatusForm
    model = Parcel

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse("parcel-detail", kwargs={"pk": self.object.pk})

class ParcelUpdateView(UpdateView, LoginRequiredMixin):
    model = Parcel
    fields = ["type", "room", "contents", "photo", "weight", "status"]

class ParcelDeleteView(DeleteView, LoginRequiredMixin):
    model = Parcel
    success_url = reverse_lazy("move-detail")