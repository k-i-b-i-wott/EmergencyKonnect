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
    return render(request,'index.html')


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



# def request_view(request, service_name):
#     submitted = False
#     if request.method == 'POST':
#         form = RequestForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('/services?submitted=true ')
#     else:
#         form = RequestForm
#         if 'submitted' in request.GET:
#             submitted = True
#         context = {'service_name': service_name}
#     return render(request, 'request.html', {'form': form, 'submitted': submitted})
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

def edit(request,user_id):
    emergencyRequest=get_object_or_404(UserRequest, id=user_id)
    if request.method == 'POST':
        form = RequestForm(request.POST, instance=emergencyRequest)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student updated successfully!')
            return redirect('about')
        else:
            messages.error(request, 'Please check form details')
    else:
        form = RequestForm(instance=emergencyRequest)
    return render(request, 'update.html', {'form':form, 'emergencyRequest':emergencyRequest})


def delete(request, user_id):
    emergencyRequest = get_object_or_404(UserRequest, id=user_id)
    try:
        UserRequest.delete()
        messages.success(request, 'Request deleted successfully!')
    except Exception as e:
        messages.error(request, 'Request was not deleted')
    return redirect('services')