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
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
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
import re

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
        for i in range(len(history)):
            if history[i]["name"] == "Edit Profile":
                history.pop(i)
                break
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

            parcels_query = Parcel.objects.filter(move_id__in=moves).aggregate(
                packed=Count("id", filter=Q(status="Packed")),
                in_transit=Count("id", filter=Q(status="In Transit")),
                lost=Count("id", filter=Q(status="Lost")),
                received=Count("id", filter=Q(status="Received")),
                damaged=Count("id", filter=Q(status="Damaged")),
                accepted=Count("id", filter=Q(status="Accepted"))
            )

            parcels = {}
            if len(parcels_query) > 0:
                for key, value in parcels_query.items():
                    new_key = re.sub("_", " ", key.title())
                    parcels[new_key] = value
            else:
                parcels = {
                    "Packed": 0,
                    "In Transit": 0,
                    "Lost": 0,
                    "Received": 0,
                    "Damaged": 0,
                    "Accepted": 0
                }
            
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

    def get_queryset(self):
        path = self.request.path_info.split("/")
        user_id = path[2]
        qs = User.objects.select_related("userprofile").filter(pk=user_id)
        return qs

class MoveListView(SitemapMixin, LoginRequiredMixin, ListView):
    paginate_by = 10
    context_object_name = "moves"

    def get_queryset(self):
        user = User.objects.get(pk=self.request.user.id)
        moves = Move.objects.select_related("primary_user").filter(Q(primary_user=user) | Q(secondary_users__in=[user])).order_by("-start_date")
        return moves
    
    def get(self, request, *args, **kwargs):
        url = request.path
        user = User.objects.select_related("userprofile").get(id=request.user.id)
        history = user.userprofile.recent_pages
        for i in range(len(history)):
            if history[i]["name"] == "My Moves":
                history.pop(i)
                break
        history.insert(0, { "name": "My Moves", "url": url })
        while len(history) > 10:
            history.pop()
        user.userprofile.recent_pages = history
        user.userprofile.save()
        return super().get(request, *args, **kwargs)

class MoveDetailView(SitemapMixin, LoginRequiredMixin, DetailView):
    model = Move

    def get_context_data(self, **kwargs):
        move_id = get_object_or_404(Move, pk=self.kwargs["pk"])

        context = super().get_context_data(**kwargs)
        parcels = Parcel.objects.filter(move_id=move_id)
        context["parcels"] = parcels
        parcel_status_query = parcels.aggregate(
            packed=Count("id", filter=Q(status="Packed")),
            in_transit=Count("id", filter=Q(status="In Transit")),
            lost=Count("id", filter=Q(status="Lost")),
            received=Count("id", filter=Q(status="Received")),
            damaged=Count("id", filter=Q(status="Damaged")),
            accepted=Count("id", filter=Q(status="Accepted"))
        )
        
        parcel_status = {}
        if len(parcel_status_query) > 0:
            for key, value in parcel_status_query.items():
                new_key = re.sub("_", " ", key.title())
                parcel_status[new_key] = value
        else:
            parcel_status = {
                "Packed": 0,
                "In Transit": 0,
                "Lost": 0,
                "Received": 0,
                "Damaged": 0,
                "Accepted": 0
            }
        
        context["parcel_status"] = parcel_status

        return context
    
    def get(self, request, *args, **kwargs):
        url = request.path
        user = User.objects.select_related("userprofile").get(id=request.user.id)
        nickname = self.get_object().nickname.strip()
        page_name = f"Move : {nickname}"
        history = user.userprofile.recent_pages
        for i in range(len(history)):
            if history[i]["name"] == page_name:
                history.pop(i)
                break
        history.insert(0, { "name": page_name, "url": url })
        while len(history) > 10:
            history.pop()
        user.userprofile.recent_pages = history
        user.userprofile.save()
        return super().get(request, *args, **kwargs)

class MoveCreateView(SitemapMixin, LoginRequiredMixin, CreateView):
    model = Move
    fields = ["nickname", "secondary_users", "start_date", "end_date", "origin_address1", "origin_address2", "origin_city", "origin_state_province", "origin_postal_code", "origin_country", "destination_address1", "destination_address2", "destination_city", "destination_state_province", "destination_postal_code", "destination_country"]
    template_name = "tracker/move_create.html"
    success_url = reverse_lazy("tracker:moves-list")

    def get(self, request, *args, **kwargs):
        url = request.path
        user = User.objects.select_related("userprofile").get(id=request.user.id)
        history = user.userprofile.recent_pages
        for i in range(len(history)):
            if history[i]["name"] == "New Move":
                history.pop(i)
                break
        history.insert(0, { "name": "New Move", "url": url })
        while len(history) > 10:
            history.pop()
        user.userprofile.recent_pages = history
        user.userprofile.save()
        return super().get(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.primary_user = self.request.user
        return super().form_valid(form)

class MoveUpdateView(SitemapMixin, LoginRequiredMixin, UpdateView):
    model = Move
    fields = ["nickname", "secondary_users", "start_date", "end_date", "origin_address1", "origin_address2", "origin_city", "origin_state_province", "origin_postal_code", "origin_country", "destination_address1", "destination_address2", "destination_city", "destination_state_province", "destination_postal_code", "destination_country"]
    template_name = "tracker/move_update.html"
    
    def get_success_url(self):
        url = reverse("tracker:move-detail", kwargs={'pk': self.get_object().id})
        return url

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.request = self.request
        return form
    
    def get(self, request, *args, **kwargs):
        url = request.path
        user = User.objects.select_related("userprofile").get(id=request.user.id)
        history = user.userprofile.recent_pages
        for i in range(len(history)):
            if history[i]["name"] == f"Edit Move: {self.get_object().nickname.strip()}":
                history.pop(i)
                break
        history.insert(0, { "name": f"Edit Move: {self.get_object().nickname.strip()}", "url": url })
        while len(history) > 10:
            history.pop()
        user.userprofile.recent_pages = history
        user.userprofile.save()
        return super().get(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.primary_user = self.request.user
        return super().form_valid(form)

class MoveDeleteView(SitemapMixin, LoginRequiredMixin, DeleteView):
    model = Move
    success_url = reverse_lazy("tracker:moves-list")

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({ "success_url": self.success_url })

class ParcelDetailView(SitemapMixin, LoginRequiredMixin, UpdateView):
    model = Parcel
    template_name = "tracker/parcel_detail.html"
    form_class = ParcelStatusForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        success = self.request.GET.get("success", None)
        if success is not None:
            context["success"] = success
        return context
    
    def get(self, request, *args, **kwargs):
        url = request.path
        user = User.objects.select_related("userprofile").get(id=request.user.id)
        history = user.userprofile.recent_pages
        for i in range(len(history)):
            if history[i]["name"] == f"Parcel Detail: {self.get_object().id}":
                history.pop(i)
                break
        history.insert(0, { "name": f"Parcel Detail: {self.get_object().id}", "url": url})
        while len(history) > 10:
            history.pop()
        user.userprofile.recent_pages = history
        user.userprofile.save()
        return super().get(request, *args, **kwargs)
    
    def get_success_url(self):
        url = reverse("tracker:parcel-detail", kwargs={'move_id': self.get_object().move_id.id, 'pk': self.get_object().id})
        url += "?success=true"
        return url

class ParcelCreateView(SitemapMixin, LoginRequiredMixin, CreateView):
    model = Parcel
    fields = ["type", "room", "contents", "photo", "weight"]
    template_name = "tracker/parcel_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get("pk")
        context["move"] = get_object_or_404(Move, pk=pk)
        return context

    def get(self, request, *args, **kwargs):
        url = request.path
        move_pk = kwargs.get('pk')
        move = get_object_or_404(Move, pk=move_pk)
        user = User.objects.select_related("userprofile").get(id=request.user.id)
        history = user.userprofile.recent_pages
        for i in range(len(history)):
            if history[i]["name"] == f"{move.nickname}: New Parcel":
                history.pop(i)
                break
        history.insert(0, { "name": f"{move.nickname}: New Parcel", "url": url })
        while len(history) > 10:
            history.pop()
        user.userprofile.recent_pages = history
        user.userprofile.save()
        return super().get(request, *args, **kwargs)
    
    def form_valid(self, form):
        pk = self.kwargs.get('pk')
        move = get_object_or_404(Move, pk=pk)
        instance = form.save(commit=False)
        instance.move_id = move
        instance.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        url = reverse("tracker:move-detail", kwargs={"pk": self.kwargs.get("pk")})
        return url

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
    template_name = "tracker/parcel_update.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        move_id = self.kwargs.get("move_id")
        context["move"] = get_object_or_404(Move, pk=move_id)
        return context

    def get_success_url(self):
        url = reverse("tracker:parcel-detail", kwargs={'move_id': self.kwargs['move_id'], 'pk': self.get_object().id})
        return url

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.request = self.request
        return form
    
    def get(self, request, *args, **kwargs):
        url = request.path
        user = User.objects.select_related("userprofile").get(id=request.user.id)
        history = user.userprofile.recent_pages
        for i in range(len(history)):
            if history[i]["name"] == f"Edit Parcel: {self.kwargs['pk']}":
                history.pop(i)
                break
        history.insert(0, { "name": f"Edit Parcel: {self.kwargs['pk']}", "url": url })
        while len(history) > 10:
            history.pop()
        user.userprofile.recent_pages = history
        user.userprofile.save()
        return super().get(request, *args, **kwargs)

class ParcelDeleteView(SitemapMixin, LoginRequiredMixin, DeleteView):
    model = Parcel

    def get_success_url(self):
        url = reverse("tracker:move-detail", kwargs={"pk": self.kwargs["move_id"]})
        return url

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({ "success_url": self.get_success_url() })

class ReceivingView(SitemapMixin, LoginRequiredMixin, TemplateView):
    template_name="tracker/receiving.html"

class LabelPreview(TemplateView):
    template_name="tracker/labels.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        move_id = self.request.GET.get('move_id', None)
        pk = self.request.GET.get('pk', None)
        if move_id is None:
            context['parcels'] = Parcel.objects.filter(move_id=pk)
        else:
            context['object'] = Parcel.objects.get(pk=pk)
        return context

class ShipParcelsView(View):
    def patch(self, request, *args, **kwargs):
        try:
            move_id = kwargs.get('move_id', None)
            if move_id is None:
                return HttpResponse("Move ID is required", status=400)
            move = get_object_or_404(Move, pk=move_id)
            parcels = Parcel.objects.filter(move_id=move, status="Packed")
            ids = []
            if len(parcels) > 0:
                for parcel in parcels:
                    ids.append(parcel.id)
                parcels.update(status="In Transit")
                parcel_list = []
                qs = Parcel.objects.filter(move_id=move, id__in=ids)
                for parcel in qs:
                    parcel_dict = parcel.__dict__.copy()
                    _ = parcel_dict.pop("_state")
                    parcel_list.append(parcel_dict)
            return JsonResponse(parcel_list, safe=False)
        except Exception as e:
            print(e)
            return HttpResponse(e, status=500)

class EndReceivingView(View):
    def patch(self, request, *args, **kwargs):
        try:
            move_id = kwargs.get('move_id', None)
            if move_id is None:
                return HttpResponse("Move ID is required", status=400)
            move = get_object_or_404(Move, pk=move_id)
            status_list = ["Accepted", "Damaged", "Received", "Lost"]
            parcels = Parcel.objects.filter(move_id=move).exclude(status__in=status_list)
            ids = []
            if len(parcels) > 0:
                for parcel in parcels:
                    ids.append(parcel.id)
                parcels.update(status="Lost")
                parcel_list = []
                qs = Parcel.objects.filter(move_id=move, id__in=ids)
                for parcel in qs:
                    parcel_dict = parcel.__dict__.copy()
                    _ = parcel_dict.pop("_state")
                    parcel_list.append(parcel_dict)
            return JsonResponse(parcel_list, safe=False)
        except Exception as e:
            print(e)
            return HttpResponse(e, status=500)