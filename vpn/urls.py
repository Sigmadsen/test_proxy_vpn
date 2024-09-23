from django.urls import path
from . import views

urlpatterns = [
    path("", views.register, name="register"),
    path("login/", views.DashboardLoginView.as_view(), name="login"),
    path("dashboard/user_info/", views.UserInfoView.as_view(), name="user_info"),
    path("dashboard/stats/", views.StatsView.as_view(), name="stats"),
    path("dashboard/add_site/", views.AddSiteView.as_view(), name="add_site"),
    path(
        "<str:user_site_name>/<path:path>/",
        views.dynamic_proxy_view,
        name="dynamic_proxy_view",
    ),
    # re_path(r'^(?P<user_site_name>[^/]+)/(?P<path>.*)$', views.dynamic_proxy_view, name='dynamic_proxy_view'),
]
