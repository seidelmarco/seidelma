from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import ArticleVotes

# Create your views here.

def votes(request, pk=None):

    #article_id = request.POST.get('id')
    #vote_type = request.POST.get('type')
    #vote_action = request.POST.get('action')

    #smallad = get_object_or_404(SmalladVotes, pk=smallad_id)
    articles = ArticleVotes.objects.all()



    template_name = 'votes/votes.html'
    #num_votes = article.userUpVotes.count() - article.userDownVotes.count()
    ctx = {'articles': articles,}

    return render(request, template_name, ctx)
