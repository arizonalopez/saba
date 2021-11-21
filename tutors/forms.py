from django.forms import ModelForm
from .models import Login, ImportantDate, UserProfile
from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field

class NameForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def validate_username(self, name):
        username = Register.objects.filter(name=name)
        data = self.cleaned_data['name']
        if data in username.name:
            raise ValidationError('Please enter another username')
        return username

class Form_supervisor(ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'

class LoginForm(forms.Form):
    name = forms.CharField(label='Name', max_length=30)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    '''def clean(self):
        cleaned_data = super().clean()
        password_1 = self.cleaned_data['password_1']
        password_2 = self.cleaned_data['password_2']
        if password_1 != password_2:
            raise forms.ValidationError('Passwords are not identical')
        return self.cleaned_data'''


    
        


'''class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline navbar-form pull-right'
        self.helper.form_id = 'signin-form'
        self.helper.form_show_labels = True
        self.helper.form_show_errors = True
        self.helper.layout = Layout(
            Field('username', placeholder="Username", autofocus=""),
            Field('password', placeholder="Password"),
            Submit('sign_in', 'Sign in', css_class="btn-sm btn-success"),
            )'''

class PersonDetailsForm(forms.Form):
    name = forms.CharField(max_length=100)
    age = forms.IntegerField()

class ImportantDateForm(forms.ModelForm):
    class Meta:
        model = ImportantDate
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout.append(Submit('save', 'Save'))

    
        