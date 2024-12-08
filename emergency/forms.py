from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User
from django import forms

from emergency.models import UserRequest


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email','class':'form-control'} ))
    username = forms.CharField(max_length= 50,widget=forms.TextInput(attrs={'placeholder': 'UserName','class':'form-control'} ) )
    gender = forms.Select(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    # image = forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control'}))
    location = forms.CharField(max_length= 50,widget=forms.TextInput(attrs={'placeholder': 'Enter your location','class':'form-control'} ))
    phone = forms.CharField(max_length= 50,widget=forms.TextInput(attrs={'placeholder': 'Enter your phone number','class':'form-control'} ))



    class Meta:
        model = User
        fields = ('username', 'email', 'location', 'phone' , 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs = {'class':'form-control'}
        self.fields['password2'].widget.attrs = {'class': 'form-control'}

    # class RequestForm(forms.ModelForm):
    #     class Meta:
    #         model = UserRequest
    #         fields = '__all__'

            # widgets = {
            #     'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email', 'name':'email'}),
            #     'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Phone Number','name':'phone'}),
            #     'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the location ','name':'location'}),
            #     'issue': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your issue ','name':'issue'}),
            # }


# class RequestForm(forms.ModelForm):
#     class Meta:
#
#         model = UserRequest
#         # fields = '__all__'
#         widgets = {
#             'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email', 'name': 'email'}),
#             'phone': forms.TextInput(
#                 attrs={'class': 'form-control', 'placeholder': 'Enter Your Phone Number', 'name': 'phone'}),
#             'location': forms.TextInput(
#                 attrs={'class': 'form-control', 'placeholder': 'Enter the location ', 'name': 'location'}),
#             'issue': forms.Textarea(
#                 attrs={'class': 'form-control', 'placeholder': 'Enter your issue ', 'name': 'issue'}),
#         }
class RequestForm(forms.ModelForm):
    class Meta:
        model = UserRequest
        fields = ['email', 'phone', 'location', 'issue']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Phone Number'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the location'}),
            'issue': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your issue'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = False
