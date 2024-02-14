from django.urls import path
from .views import HomePageView, SignUpView, LoginView, DashboardView, UserListView, UserDetailView, MoveListView, MoveDetailView, ParcelListView, ParcelDetailView

app_name = "tracker"

urlpatterns = [
    path("", HomePageView.as_View(), name="home"),
    path("sign-up/", SignUpView.as_View(), name="sign-up"),
    path("login/", LoginView.as_View(), name="login"),
    path("dashboard/", DashboardView.as_View(), name="dashboard"),
    path("users/", UserListView.as_View(), name="users-list"),
    path("users/<int:pk>/", UserDetailView.as_View(), name="user-detail"),
    path("moves/", MoveListView.as_View(), name="moves-list"),
    path("moves/<int:pk>/", MoveDetailView.as_view(), name="move-detail"),
    path("parcels/", ParcelListView.as_view(), name="parcels-list"),
    path("parcels/<int:pk>/", ParcelDetailView.as_view(), name="parcel-detail")
]