# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect


def index(request):
    if request.user.is_authenticated():
        return redirect('users-dashboard')
    return render(request, "index.html", {
    })
