# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView, ListView, DetailView

from braces.views import LoginRequiredMixin

from .forms import UserForm


class UserListView(ListView):
    queryset = User.objects.all().order_by('username')
    context_object_name = 'users'
    paginate_by = 10
    template_name = "users/user_list.html"


class UserProfileView(DetailView):
    model = User
    slug_url_kwarg = slug_field = 'username'
    context_object_name = 'user_obj'
    template_name = "users/profile.html"


class LoginView(TemplateView):
    template_name = "users/login.html"


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "users/dashboard.html"


class EditAccountsView(LoginRequiredMixin, TemplateView):
    template_name = "users/edit_accounts.html"


@login_required
def edit_profile(request):
    initial = {
        'debug': request.user.get_profile().debug,
    }
    form = UserForm(request.POST or None, instance=request.user, initial=initial)
    if form.is_valid():
        form.save()
        messages.success(request, _(u"Profile information has been updated."))
        return redirect('users-edit_profile')
    return render(request, "users/edit_profile.html", {
        'form': form,
    })

