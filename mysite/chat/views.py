from chat.models import Message
from django.views import View

from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.humanize.templatetags.humanize import naturaltime
import time


class HomeView(View) :
    def get(self, request):
        return render(request, 'chat/main.html')

def jsonfun(request):
    time.sleep(2)
    stuff = {
        'first': 'first thing',
        'second': 'second thing'
    }
    return JsonResponse(stuff)


class TalkMain(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'chat/talk.html')

    def post(self, request):
        message = Message(text=request.POST['message'], owner=request.user)
        message.save()
        return redirect(reverse('chat:talk'))


class TalkMessages(LoginRequiredMixin, View):
    def get(self, request):
        messages = Message.objects.all().order_by('-created_at')[:10]
        results = []
        for message in messages:
            result = [message.text, naturaltime(message.created_at)]
            results.append(result)
        return JsonResponse(results, safe=False)
