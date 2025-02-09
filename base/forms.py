from django.forms import ModelForm
from .models import Room ,Topic ,Message
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class Roomform(ModelForm):
    participants = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host','topic']

class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15, required=False)
    qualifications = forms.CharField(widget=forms.Textarea, required=False)
    address = forms.CharField(widget=forms.Textarea, required=False)
    image = forms.ImageField(required=False)  # New image field

    class Meta:
        model = User
        fields = ('first_name','last_name','email', 'phone_number', 'qualifications', 'address', 'password1', 'password2','image')

class Topicform(ModelForm):
    class Meta:
        model = Topic
        fields = ('Topic_name',)


class MessageForm(forms.ModelForm): 
    class Meta: 
        model = Message 
        fields = ['body', 'image', 'file', 'video', 'audio', 'link']


class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'qualifications', 'address', 'image')