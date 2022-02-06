from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, reverse
import datetime
from django.utils import timezone
from django.db.models import F

from django.contrib.auth.decorators import login_required
from django.views import generic, View


from polls.models import Question, Choice
from .models import Blog, Entry, Author, Post, Comment
from dataproject.models import Keydata
from .forms import PostForm, CommentForm, NewUserForm

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.humanize.templatetags.humanize import naturaltime

from django.contrib.auth import login
from django.contrib import messages

from django.conf import settings


'''
#PRojekt rewriting HomeView(View)

Achtung: an ad_list-view orientieren was von owner_list view erbt owner.py
anlegen und classbased view benutzen


class HomeView(View) :
    def get(self, request):
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[:5]
        latest_keydata_list = Keydata.objects.values().order_by('-divyield')[:7]
        vote_one_question = Question.objects.get(latest_poll=True)
        messages = HomeMessage.objects.all().order_by('-created_at')[:10]
        results = []
        for message in messages:
            result = [message.text, naturaltime(message.created_at)]
            results.append(result)
        jsondump = JsonResponse(results, safe=False)
        context = {
        'posts': posts,
        'latest_keydata_list': latest_keydata_list,
        'vote_one_question': vote_one_question,
        'jsondump': jsondump,
        }
        return render(request, 'home.html', ctx)


class TalkMain(LoginRequiredMixin, View) :
    def get(self, request):
        return render(request, 'chat/talk.html')

    def post(self, request) :
        message = Message(text=request.POST['message'], owner=request.user)
        message.save()
        return redirect(reverse('chat:talk'))

class TalkMessages(LoginRequiredMixin, View) :
    def get(self, request):
        messages = Message.objects.all().order_by('-created_at')[:10]
        results = []
        for message in messages:
            result = [message.text, naturaltime(message.created_at)]
            results.append(result)
        return JsonResponse(results, safe=False)
'''

def register_request(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            #das ist doch nur für die console??? Ich brauche eine success-url
            # die messages werden z. B. im Admin-Panel angezeigt
            messages.success(request, 'Registration successful.')
            # durch das reverse brauche ich erst einmal keine success-page
            return redirect(reverse('home'))
        messages.error(request, 'Unsuccessful registration. Invalid information.')
    form = NewUserForm()
    return render (request=request, template_name="registration/register.html", context={"register_form":form})

'''
If you're looking for access to other constants in the settings, then simply unpack the constants you want and add them to the context dictionary you're using in your view function, like so:

from django.conf import settings
from django.shortcuts import render_to_response

def my_view_function(request, template='my_template.html'):
    context = {'favorite_color': settings.FAVORITE_COLOR}
    return render_to_response(template, context)
Now you can access settings.FAVORITE_COLOR on your template as {{ favorite_color }}.
'''

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[:5]
    latest_keydata_list = Keydata.objects.values().order_by('-divyield')[:7]
    vote_one_question = Question.objects.get(latest_poll=True)
    try:
        selected_choice = vote_one_question.choice_set.get(pk=request.POST['choice']) #string choice ist der name aus dem html-form, request.POST greift auf den key 'choice' eines dicts zu
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'home.html', {
            'posts': posts,
            'latest_keydata_list': latest_keydata_list,
            'vote_one_question': vote_one_question,
            'error_message': "You didn't select a choice.",
            })
    else:
        selected_choice.votes += 1  #.votes kommt aus dem Model Choice
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return redirect('polls:results', vote_one_question.id,)
    #vote_one_question = Question.objects.filter(pub_date__gte=datetime.date.today())
    context = {
        'posts': posts,
        'latest_keydata_list': latest_keydata_list,
        'vote_one_question': vote_one_question,
        'app_name': settings.APP_NAME,
        }
    return render(request, 'home.html', context)


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
        ctx = {'form': form}
    return render(request, 'add_comment_to_post.html', ctx)


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    ctx = {
        'post': post
        }
    return render(request, 'post_detail.html', ctx)


@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
        ctx = {'form': form}
    return render(request, 'post_edit.html', ctx)


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'post_edit.html', {'form': form})


@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('-created_date')
    ctx = {'posts': posts}
    return render(request, 'post_draft_list.html', ctx)


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


@login_required
def post_remove(request,pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[:5]
    ctx = {'posts': posts}
    return render(request, 'home.html', ctx)


#meine alte Variante mit fehlerhaften Querysets - debuggen:
'''
def post_list(request):
    authors_list = Author.objects.all()
    latest_entry_list = Entry.objects.order_by('-pub_date')[:5]
    #authors = latest_entry_list.authors.all()
    latest_blog_list = Blog.objects.order_by('name')[:5]
    context = {
        'authors_list': authors_list,
        'latest_entry_list': latest_entry_list,
        'latest_blog_list': latest_blog_list,
        }
    return render(request, 'blog/post_list.html', context)
'''


# References

# https://simpleisbetterthancomplex.com/tutorial/2016/07/27/how-to-return-json-encoded-response.html
