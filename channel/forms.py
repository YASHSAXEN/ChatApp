from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from channel.models import ChatMessages

class SignUp(UserCreationForm):
    usable_password = None
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter the password', 'class':'field'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Re enter the password', 'class':'field'}))
    class Meta(UserCreationForm.Meta):
        fields = ['username','email','first_name','last_name']
        widgets ={
            'username':forms.TextInput(attrs={'placeholder':'Enter the username', 'class':'field'}),
            'email':forms.EmailInput(attrs={'placeholder':'Enter the email id', 'class':'field'}),
            'first_name':forms.TextInput(attrs={'placeholder':'Enter the first name', 'class':'field'}),
            'last_name':forms.TextInput(attrs={'placeholder':'Enter the last name', 'class':'field'}),
        }

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter the username', 'class':'field'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter the password', 'class':'field'}))

class FileForm(forms.ModelForm):
    class Meta:
        model = ChatMessages
        fields = ['user','file',"groupname",'message']
        widgets = {'user':forms.TextInput(attrs={'hidden':True}),
                   'groupname':forms.TextInput(attrs={'hidden':True}),
                   'message':forms.TextInput(attrs={'hidden':True})}