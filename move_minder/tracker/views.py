from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from django.contrib.auth.models import User
from django.contrib.sites.requests import RequestSite
from django.contrib.sites.models import Site
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.base import TemplateView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import ParcelStatusForm, SignUpForm
from .models import Move, Parcel, UserProfile
from phonenumber_field.formfields import PhoneNumberField
from move_minder.sitemaps import StaticViewSitemap

# Create your views here.
class SitemapMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request_site = RequestSite(self.request)

        try:
            current_site = Site.objects.get_current(request_site)
        except ImproperlyConfigured:
            current_site = None

        context['current_site'] = current_site
        sitemap = StaticViewSitemap(request_site=request_site, current_site=current_site)
        context['sitemap'] = sitemap.get_urls()

        for url in context['sitemap']:
            url['name'] = " ".join(url['item'].split(":")[-1].split("-")).title()
        return context

class HomePageView(SitemapMixin, TemplateView):
    template_name = "tracker/home.html"

    """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # add additional context as necessary
        return context
    """

class SignupView(SitemapMixin, CreateView):
    model = UserProfile
    template_name = "tracker/signup.html"
    success_url = reverse_lazy('login')
    form_class = SignUpForm

class UserUpdateView(SitemapMixin, LoginRequiredMixin, UpdateView):
    model = User
    fields = ["first_name", "last_name", "username", "password", "password", "email", "phone"]

class DashboardView(SitemapMixin, LoginRequiredMixin, TemplateView):
    template_name = "tracker/dashboard.html"

class UserListView(SitemapMixin, LoginRequiredMixin, ListView):
    model = User
    paginate_by = 50
    context_object_name = "users"

class UserDetailView(SitemapMixin, LoginRequiredMixin, DetailView):
    model = User

class MoveListView(SitemapMixin, LoginRequiredMixin, ListView):
    paginate_by = 10
    context_object_name = "moves"

    def get_queryset(self):
        user_id = self.request.user.id
        return Move.objects.filter(Q(primary_user=user_id) | Q(secondary_users__contains=user_id))

class MoveDetailView(SitemapMixin, LoginRequiredMixin, DetailView):
    model = Move

    def get_context_data(self, **kwargs):
        # path_list = self.request.path.split("/")
        # move_id = path_list[2]
        move_id = get_object_or_404(Move, pk=self.kwargs["pk"])

        context = super().get_context_data(**kwargs)
        context["parcels"] = Parcel.objects.filter(move_id=move_id)

        return context

class MoveCreateView(SitemapMixin, LoginRequiredMixin, CreateView):
    model = Move
    fields = ["nickname", "secondary_users", "start_date", "end_date", "origin_address1", "origin_address2", "origin_city", "origin_state_province", "origin_postal_code", "origin_country", "destination_address1", "destination_address2", "destination_city", "destination_state_province", "destination_postal_code", "destination_country"]

class MoveUpdateView(SitemapMixin, LoginRequiredMixin, UpdateView):
    model = Move
    fields = ["nickname", "secondary_users", "start_date", "end_date", "origin_address1", "origin_address2", "origin_city", "origin_state_province", "origin_postal_code", "origin_country", "destination_address1", "destination_address2", "destination_city", "destination_state_province", "destination_postal_code", "destination_country"]

class MoveDeleteView(SitemapMixin, LoginRequiredMixin, DeleteView):
    model = Move
    success_url = reverse_lazy("moves-list")

class ParcelDetailView(SitemapMixin, LoginRequiredMixin, DetailView):
    model = Parcel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ParcelStatusForm()
        return context

class ParcelCreateView(SitemapMixin, LoginRequiredMixin, CreateView):
    model = Parcel
    fields = ["type", "room", "contents", "photo", "weight"]

class ParcelStatusUpdateView(SitemapMixin, LoginRequiredMixin, SingleObjectMixin, FormView):
    template_name = "tracker/parcel_detail.html"
    form_class = ParcelStatusForm
    model = Parcel

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse("parcel-detail", kwargs={"pk": self.object.pk})

class ParcelUpdateView(SitemapMixin, LoginRequiredMixin, UpdateView):
    model = Parcel
    fields = ["type", "room", "contents", "photo", "weight", "status"]

class ParcelDeleteView(SitemapMixin, LoginRequiredMixin, DeleteView):
    model = Parcel
    success_url = reverse_lazy("move-detail")

class ParcelScanView(SitemapMixin, LoginRequiredMixin, TemplateView):
    template_name="tracker/parcel-scan.html"