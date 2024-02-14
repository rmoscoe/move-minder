from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# Create your views here.
class HomePageView(View):
    pass

class SignupView(FormView):
    pass

class DashboardView(View, LoginRequiredMixin):
    pass

class UserListView(ListView, LoginRequiredMixin):
    pass

class UserDetailView(DetailView, LoginRequiredMixin):
    pass

class MoveListView(ListView, LoginRequiredMixin):
    pass

class MoveDetailView(DetailView, LoginRequiredMixin):
    pass

class MoveUpdateView(UpdateView, LoginRequiredMixin):
    pass

class MoveDeleteView(DeleteView, LoginRequiredMixin):
    pass

class ParcelListView(ListView, LoginRequiredMixin):
    pass 

class ParcelDetailView(DetailView, LoginRequiredMixin):
    pass

class ParcelUpdateView(UpdateView, LoginRequiredMixin):
    pass

class ParcelDeleteView(DeleteView, LoginRequiredMixin):
    pass