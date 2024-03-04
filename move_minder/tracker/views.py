from datetime import date
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.sites.requests import RequestSite
from django.contrib.sites.models import Site
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Q, Count
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.base import TemplateView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import ParcelStatusForm, SignUpForm, UpdateUserForm, MoveForm, ParcelForm
import json
from .models import Move, Parcel, UserProfile
from move_minder.sitemaps import StaticViewSitemap
import os
from phonenumber_field.formfields import PhoneNumberField

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
    
class AnonymousUserMixin(UserPassesTestMixin):
    def test_func(self):
        return not self.request.user.is_authenticated
    
    def handle_no_permission(self):
        return HttpResponseRedirect(reverse_lazy("tracker:dashboard"))

class HomePageView(SitemapMixin, TemplateView):
    template_name = "tracker/home.html"

    """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # add additional context as necessary
        return context
    """

class SignupView(SitemapMixin, AnonymousUserMixin, CreateView):
    model = UserProfile
    template_name = "tracker/signup.html"
    success_url = reverse_lazy('login')
    form_class = SignUpForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = context.get("form")
        if form:
            context["form_errors"] = form.errors
        return context
    
    def form_valid(self, form):
        user = form.save()
        phone = form.cleaned_data["phone"]
        UserProfile.objects.create(user=user, phone=phone)
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

class CustomLoginView(SitemapMixin, AnonymousUserMixin, LoginView):
    model = UserProfile
    template_name = "tracker/login.html"
    success_url = reverse_lazy("tracker:dashboard")
    form_class = AuthenticationForm

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

class UserUpdateView(SitemapMixin, LoginRequiredMixin, UpdateView):
    model = User
    template_name = "tracker/user_update.html"
    form_class = UpdateUserForm

    def get_initial(self):
        initial = super().get_initial()
        user = self.get_object()
        profile = UserProfile.objects.get(user=user)
        initial["phone"] = profile.phone
        return initial

    def get_success_url(self):
        return reverse("tracker:user-detail", kwargs={"pk": self.request.user.id})
    
    def get(self, request, *args, **kwargs):
        url = request.path
        user = User.objects.select_related("userprofile").get(id=request.user.id)
        history = user.userprofile.recent_pages
        history.insert(0, { "name": "Edit Profile", "url": url })
        while len(history) > 10:
            history.pop()
        user.userprofile.recent_pages = history
        user.userprofile.save()
        return super().get(request, *args, **kwargs)
    
    def form_valid(self, form):
        user = form.save()
        phone = form.cleaned_data["phone"]
        UserProfile.objects.filter(user=user).update(phone=phone)
        return super().form_valid(form)

class DashboardView(SitemapMixin, LoginRequiredMixin, TemplateView):
    template_name = "tracker/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = date.today()
        try:
            user_id = self.request.user.id
            moves = Move.objects.filter(
                Q(primary_user=user_id) | Q(secondary_users__in=[user_id]),
            )

            upcoming = moves.filter(
                start_date__gte=today
            ).values(
                "id",
                "nickname",
                "start_date",
                "primary_user__first_name",
                "primary_user__last_name",
                "origin_city",
                "destination_city"
            ).order_by(
                "start_date", 
                "origin_city", 
                "destination_city"
            )
            context["moves"] = upcoming[:10]

            parcels = Parcel.objects.filter(move_id__in=moves).annotate(
                packed=Count("id", filter=Q(status="Packed")),
                in_transit=Count("id", filter=Q(status="In Transit")),
                lost=Count("id", filter=Q(status="Lost")),
                received=Count("id", filter=Q(status="Received")),
                damaged=Count("id", filter=Q(status="Damaged")),
                accepted=Count("id", filter=Q(status="Accepted"))
            ).values(
                "packed",
                "in_transit",
                "lost",
                "received",
                "damaged",
                "accepted"
            )
            context["parcels"] = parcels

            recent = UserProfile.objects.filter(user=user_id).values("recent_pages")
            recent_pages = list(recent)[0]["recent_pages"][:10]
            context["recent_pages"] = recent_pages
            
        except Exception as e:
            print(e)
        return context

class UserListView(SitemapMixin, LoginRequiredMixin, ListView):
    model = User
    paginate_by = 50
    context_object_name = "users"

class UserDetailView(SitemapMixin, LoginRequiredMixin, DetailView):
    model = User
    template_name = "tracker/user_detail.html"

class MoveListView(SitemapMixin, LoginRequiredMixin, ListView):
    paginate_by = 10
    context_object_name = "moves"

    def get_queryset(self):
        user_id = self.request.user.id
        return Move.objects.filter(Q(primary_user=user_id) | Q(secondary_users__in=[user_id]))
    
    def get(self, request, *args, **kwargs):
        url = request.path
        user = User.objects.select_related("userprofile").get(id=request.user.id)
        history = user.userprofile.recent_pages
        history.insert(0, { "name": "My Moves", "url": url })
        while len(history) > 10:
            history.pop()
        user.userprofile.recent_pages = history
        user.userprofile.save()
        return super().get(request, *args, **kwargs)

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