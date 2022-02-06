from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.http import urlencode
from django.http import HttpResponse

# Create your views here.

class DumpPython(View):
    def get(self, req):
        resp = "<p>We want to transfer the user to a login page from many pages\n"
        resp += "in our app and when they successfully log in, we want to\n"
        resp += "bring them back to our page or some other page. The next=\n"
        resp += "parameter tells login or logout where to redirect the user</p>\n"
        resp += "<pre>\nUser Data in Python: \n\n"
        resp += "Login url: " + reverse('login') + "\n"
        resp += "Logout url: " + reverse('logout') + "\n\n"
        if req.user.is_authenticated:
            resp += "User: " + req.user.username + "\n"
            resp += "Email: " + req.user.email + "\n"

        else:
            resp += "User is not logged in\n"

        resp += "\n"
        resp += "</pre>\n"
        resp += """<a href="/authz">Go back</a>"""
        return HttpResponse(resp)



class OpenView(View):
    def get(self, request):
        return render(request, 'authz/main.html')


class ApereoView(View):
    def get(self, request):
        return render(request, 'authz/main.html')


class ManualView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            loginurl = reverse('login')+'?'+urlencode({'next': request.path })
            return redirect(loginurl)
        return render(request, 'authz/main.html')


class ProtectView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'authz/main.html')

