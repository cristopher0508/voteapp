from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.db.models import Q, F
from django.contrib.auth import authenticate, login, logout
from .models import UserProfile, voteImages, Notification
from django.contrib import messages
from .forms import ProfileForm
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

def home(request):
    if request.method == 'GET':
        return render(request, 'principal.html')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is None:
            return render(request, 'principal.html', {'error': 'EL Usuario no existe'})
        else:
            try:
                login(request, user)
                usuario = request.user.profile.user_id
                if not usuario:
                    return redirect('profile-edit')
                if UserProfile.objects.filter(user_id = request.user.profile.user_id).exists():
                    return redirect('profile', usuario)
            except ObjectDoesNotExist:
                return redirect('profile-edit')

                
            
def signout(request):
    logout(request)
    return redirect('principal')

def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if User.objects.filter(email=email).exists():
                context = {'error': 'Este Usuario ya existe'}
                messages.warning(request, 'User already exist')
                return redirect('register')

            else:
                try:
                    user = User.objects.create_user(username=username, password=password1,email=email)
                    user.save()
                    login(request, user)
                    return redirect('principal')
                except ObjectDoesNotExist:
                    return redirect('principal')
            
def profileEdit(request):
    if request.method == 'GET':
        return render(request, 'profileedit.html')
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        picture = request.FILES['picture']
        user = request.user
        profile = UserProfile.objects.create(
            name = name,
            description = description,
            picture = picture,
            user = user
        )
        if profile.user == request.user:
            profile.save()
        return redirect('profile', request.user.profile.user_id)
    
def profile(request, id):
    if request.method == 'GET':
        name = request.user.profile.name
        profile = UserProfile.objects.get(user_id = id)
        followers = profile.followers.filter(id = request.user.profile.user_id)
        user = request.user.profile.user_id
        if user in followers:
            follow_button_value = 'unfollow'
        else:
            follow_button_value = 'follow'
        votes = voteImages.objects.filter(author_id = profile.user_id).order_by('-created')
        return render(request, 'profile.html', {'perfil':profile, 'votes':votes, 'follow_button_value': follow_button_value})
    
def profile_edit(request, id):
    if request.method == 'GET':
        context = {'form':ProfileForm}
        return render(request, 'profile-edit.html', context)
    if request.method == 'POST':
        profile = UserProfile.objects.get(user_id = id)
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', request.user.profile.user_id)
    
    
def voteHome(request):
    if request.method == 'GET':
        logged_in_user = request.user.profile.user_id
        vote = voteImages.objects.filter(
            author__followers__in=[logged_in_user],
        ).order_by('-created')

        notifications = Notification.objects.filter(to_user_id = request.user.profile.user_id).order_by('-created').exclude(user_has_seen = True)

        context = {'votes':vote, 'notifications':notifications}
        return render(request, 'home.html', context)
    
def allVotes(request):
    if request.method == 'GET':
        vote = voteImages.objects.all().order_by('-created')
        context = {'votes': vote}
        return render(request, 'all-votes.html', context)
    

    
    
    


def newVote(request):
    if request.method == 'GET':
        return render(request, 'newvote.html')
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        first_image = request.FILES['first_image']
        second_image = request.FILES['second_image']
        author = request.user.profile.user_id
        vote = voteImages.objects.create(
            title = title,
            description = description,
            first_image = first_image,
            second_image = second_image,
            author_id = author
        )
        vote.save()
        return redirect('home')
    
def addVote(request, id):
    if request.method == 'POST':
        votes = voteImages.objects.get(id = id)
        user = request.user.profile.user_id
        selected_option_one = request.POST.get('img', False)
        selected_option_two = request.POST.get('imgs', False)
        
        

        if selected_option_one:
            if votes.vote_image_first.filter(user_id = user).exists():
                votes.vote_image_first.remove(user)
            else:
                votes.vote_image_first.add(user)
                votes.vote_image_second.remove(user)
                notification = Notification.objects.create(notification_type = 2, to_user_id = votes.author.user_id, from_user_id = request.user.profile.user_id, vote_id = votes.id)

                
        
        next = request.POST.get('img', 'add-vote')
        votos = votes.vote_image_first.all().count()
        return HttpResponseRedirect(next)
    

def AddVoteTwo(request, id):
    if request.method == 'POST':
        votes = voteImages.objects.get(id = id)
        user = request.user.profile.user_id
        selected_option_two = request.POST

        if selected_option_two:
            if votes.vote_image_second.filter(user_id = user).exists():
                votes.vote_image_second.remove(user)
            else:
                votes.vote_image_second.add(user)
                Notification.objects.create(notification_type = 3, to_user_id = votes.author_id, from_user_id = request.user.profile.user_id, vote_id = votes.id)
                if votes.vote_image_first.filter(user_id = user).exists():
                    votes.vote_image_first.remove(user)
                    votes.vote_image_second.add(user)

        next = request.POST.get('imgs', 'add-vote-two')
        return HttpResponseRedirect(next)


def VoteDetail(request, id):
    if request.method == 'GET':
        vote = voteImages.objects.get(id=id)
        context = {'vote':vote}
        return render(request, 'votedetail.html', context)
    
    if request.method == 'POST':
        vote = voteImages.objects.get(id = id)
        vote.save()
        return redirect('vote-detail')

def delete_post(request, id):
    vote = voteImages.objects.get(id = id)
    if request.method == 'POST':
        vote.delete()
        return redirect('profile', vote.author_id)
    

def searchUser(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        profile_list = UserProfile.objects.filter(
            Q(name__icontains = query)
        ).distinct()

        context = {'profile_list': profile_list}

        return render(request, 'search.html', context)


def searchResponsive(request):
    return render(request, 'search-responsive.html')


def profileView(request, id):
    if request.method == 'GET':
        profile = UserProfile.objects.get(user_id = id)
        return redirect('profile', profile)

def addFollower(request, id):
    if request.method == 'POST':
        user = request.user.profile.user_id
        profile = UserProfile.objects.get(user_id = id)
        if profile.followers.filter(id = user).exists():
            profile.followers.remove(user)
        else:
            profile.followers.add(user)
            Notification.objects.create(notification_type = 1, to_user_id = profile.user_id, from_user_id = request.user.profile.user_id)

        next = request.POST.get('follow', 'profile')
        votos = profile.followers.all().count()
        return redirect('profile', profile.user_id)
    

    
def voteNotification(request, vote_id, notification_id):
    if request.method == 'GET':
        notification = Notification.objects.get(id=notification_id)
        vote = voteImages.objects.get(id = vote_id)

        notification.user_has_seen = True
        notification.save()

        return redirect('vote-detail', id=vote_id)
    
def followNotification(request, notification_id, profile_id):
    if request.method == 'GET':
        notification = Notification.objects.get(id=notification_id)
        profile = UserProfile.objects.get(user_id = profile_id)

        notification.user_has_seen = True
        notification.save()

        return redirect('profile', profile_id)
        
    


