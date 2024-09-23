import requests
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import TemplateView, ListView

from .forms import UserRegisterForm, UserEditForm, SiteCreateForm
from .models import Site


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Account {username} has been created!")
            return redirect("login")
    else:
        form = UserRegisterForm()
    return render(request, "users/register.html", {"form": form})


class UserInfoView(TemplateView):
    template_name = "dashboard/user_info.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["user"] = user
        form = UserEditForm(instance=user)
        context["form"] = form
        return context

    def post(self, request, *args, **kwargs):
        user = request.user
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("user_info")
        return self.render_to_response(self.get_context_data(form=form))


class StatsView(ListView):
    template_name = "dashboard/stats.html"
    context_object_name = "sites"

    def get_queryset(self):
        return Site.objects.filter(user=self.request.user).order_by("-id")


class AddSiteView(TemplateView):
    template_name = "dashboard/add_site.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sites"] = Site.objects.filter(user=self.request.user).order_by("-id")
        form = SiteCreateForm()
        context["form"] = form
        return context

    def post(self, request, *args, **kwargs):
        form = SiteCreateForm(request.POST)
        if form.is_valid():
            site = form.save(commit=False)
            site.user = request.user
            site.save()
            return redirect("add_site")
        return self.render_to_response(self.get_context_data(form=form))


class DashboardLoginView(LoginView):
    template_name = "users/login.html"
    redirect_authenticated_user = True
    redirect_field_name = "user_info"
    next_page = "user_info"


def dynamic_proxy_view(request, user_site_name, path):
    site = get_object_or_404(Site, title=user_site_name, user=request.user)

    final_url = site.original_url + path
    response = requests.get(final_url)

    data_sent = len(request.body)
    if request.META.get("CONTENT_LENGTH"):
        data_sent += int(request.META.get("CONTENT_LENGTH", 0))

    data_received = len(response.content)

    site.visit_count += 1
    site.data_sent += data_sent
    site.data_received += data_received
    site.save()

    return HttpResponse(response.content, content_type=response.headers["Content-Type"])
