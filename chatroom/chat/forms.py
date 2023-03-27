from django import forms
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.forms import UserCreationForm
# from django.core.validators import MaxValueValidator

class NewUserForm(UserCreationForm):
    phone = forms.IntegerField()
    def __init__(self, *args, **kwargs):
        super(NewUserForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    
    class Meta:
        model = User
        fields = ('first_name','last_name','email','phone','username','password1', 'password2')
        labels = {'phone': 'Phone Number',}    