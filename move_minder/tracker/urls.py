from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import HomePageView, SignupView, DashboardView, UserListView, UserDetailView, MoveListView, MoveDetailView, MoveCreateView, MoveUpdateView, MoveDeleteView,ParcelDetailView, ParcelCreateView, ParcelUpdateView, ParcelDeleteView, ParcelScanView

app_name = "tracker"

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("sign-up/", SignupView.as_view(), name="sign-up"),
    path("login/", LoginView.as_view(template_name="tracker/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("users/", UserListView.as_view(), name="users-list"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    path("moves/", MoveListView.as_view(), name="moves-list"),
    path("moves/<int:pk>/", MoveDetailView.as_view(), name="move-detail"),
    path("moves/new/", MoveCreateView.as_view(), name="move-create"),
    path("moves/<int:pk>/edit/", MoveUpdateView.as_view(), name="move-update"),
    path("moves/<int:pk>/delete/", MoveDeleteView.as_view(), name="move-delete"),
    path("parcels/<int:pk>/", ParcelDetailView.as_view(), name="parcel-detail"),
    path("parcels/new/", ParcelCreateView.as_view(), name="parcel-create"),
    path("parcels/<int:pk>/edit/", ParcelUpdateView.as_view(), name="parcel-update"),
    path("parcels/<int:pk>/delete/", ParcelDeleteView.as_view(), name="parcel-delete"),
    path("parcels/scan/", ParcelScanView.as_view(), name="parcel-scan")
]