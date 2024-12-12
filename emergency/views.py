from http.client import HTTPResponse

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse_lazy

from .forms import UserRegisterForm
from .forms import RequestForm
from django.http import HttpResponse, HttpResponseRedirect

from .models import UserRequest


# Create your views here.

def index(request):
    # Assume the logged-in user wants to see their own info
    username = request.user.username if request.user.is_authenticated else None
    return render(request, 'index.html', {'username': username})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
           form.save()
           username = request.POST.get('email')
           password = request.POST.get('password')

           # user = authenticate(request, username=username, password=password)
           # login(request, user)
           # messages.success(request, f'Account created for {username}')
           return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request,'signup.html', {'form': form})




def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user =User.objects.get(email=email)
            username = user.username
        except User.DoesNotExist:
            username=email
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.success(request, 'There was an error loging in. Try again!!')
            return redirect('login')
    else:
        return render(request,'login.html')


@login_required()
def logout_view(request):
    # if request.method == 'POST':
        logout(request)
        return redirect('index')

    # return redirect('login')


@login_required()
def services(request):
    return render(request,'services.html')

def about(request):
    return render(request,'about.html')




@login_required
def request_view(request, service_name):
    submitted = False
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            user_request = form.save(commit=False)
            user_request.email = request.user.email
            user_request.user = request.user
            user_request.save()
            return HttpResponseRedirect('/services?submitted=true')
    else:
        form = RequestForm
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'request.html', {'form': form, 'submitted': submitted})


class passwordsChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('index')

def password_success(request):
    return render(request,'password_success.html',{})


def update_view(request, user_id):
    emerge=UserRequest.objects.get(pk=user_id)

    return render(request,'update.html',{'emerge':emerge})





@login_required
def info(request, username):
    if not username:  # Redirect or raise an error if username is empty
        return render(request, 'about.html', {'message': 'Invalid username'})

    # Fetch emergencies for the user
    reported_emergencies = UserRequest.objects.filter(user__username=username)
    return render(request, 'info.html', {
        'profile_user': username,
        'reported_emergencies': reported_emergencies,
    })



def update_request(request,user_id):
    emergencyRequest=get_object_or_404(UserRequest, user_id=user_id)
    if request.method == 'POST':
        form = RequestForm(request.POST, instance=emergencyRequest)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student updated successfully!')
            return redirect('info',)
        else:
            messages.error(request, 'Please check form details')
    else:
        form = RequestForm(instance=emergencyRequest)
    return render(request, 'update.html', {'form':form, 'emergencyRequest':emergencyRequest})


from django.shortcuts import redirect, get_object_or_404
from .models import UserRequest

def delete_request(request, user_id):

    request_to_delete = get_object_or_404(UserRequest, user_id=user_id)
    username = request_to_delete.user.username
    request_to_delete.delete()
    return redirect('info', username=username)
