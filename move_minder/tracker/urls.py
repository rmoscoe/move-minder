from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import HomePageView, SignupView, LoginView, DashboardView, UserListView, UserDetailView, MoveListView, MoveDetailView, MoveUpdateView, MoveDeleteView, ParcelListView, ParcelDetailView, ParcelUpdateView, ParcelDeleteView

app_name = "tracker"

urlpatterns = [
    path("", HomePageView.as_View(), name="home"),
    path("sign-up/", SignupView.as_View(), name="sign-up"),
    path("login/", LoginView.as_View(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("dashboard/", DashboardView.as_View(), name="dashboard"),
    path("users/", UserListView.as_View(), name="users-list"),
    path("users/<int:pk>/", UserDetailView.as_View(), name="user-detail"),
    path("moves/", MoveListView.as_View(), name="moves-list"),
    path("moves/<int:pk>/", MoveDetailView.as_view(), name="move-detail"),
    path("moves/<int:pk>/edit/", MoveUpdateView.as_view(), name="move-update"),
    path("moves/<int:pk>/delete/", MoveDeleteView.as_view(), name="move-delete"),
    path("parcels/", ParcelListView.as_view(), name="parcels-list"),
    path("parcels/<int:pk>/", ParcelDetailView.as_view(), name="parcel-detail"),
    path("parcels/<int:pk>/edit/", ParcelUpdateView.as_view(), name="parcel-update"),
    path("parcels/<int:pk>/delete/", ParcelDeleteView.as_view(), name="parcel-delete")
]