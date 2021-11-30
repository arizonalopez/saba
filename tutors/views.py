from django.shortcuts import render, redirect, get_object_or_404
from .forms import NameForm, LoginForm, ImportantDateForm
from .models import Register, Login, ImportantDate, ViralVideo
from django.http import HttpResponse
from django.urls import reverse
from django.conf import settings
from braces.views import JSONResponseMixin
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
#from django.contrib.auth.decorators import login_required

# Create your views here.
def about(request):
    return render(request, 'tutors/about.html', {'title': 'about'})

'''class AboutView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'tutors/about.html'''

def register(request):
    if request.POST:
        form = NameForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            messages.success(request, f'Account created successfully for {username}')
            return redirect('login')
        else:
            return render(request, 'tutors/register.html', {'form': form})
    else:
        form = NameForm()
        return render(request, 'tutors/register.html', {'form': form})




def home(request, user_id):
    name = get_object_or_404(Register, user_id)
    return render(request, 'tutors/home.html', {'name': name})

def login(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if request.GET.get('next') is not None:
                return redirect(request.GET['next'])
            messages.success(request, 'Login successful!')
            return redirect('about')
        else:
            return HttpResponse(f'<h1>You have provided an invalid credentials for {username}</h1>') 
    else:
        form = LoginForm()
        return render(request, 'tutors/login.html', {'form': form, 'title': 'login'})

'''class LoginView(generic.View):
    model = Login
    form_class = LoginForm
    template_name = 'tutors/login.html'


    def post(self, request, *args, **kwargs):
        username = request.GET['username']
        password = request.GET['password']
        new_user = authenticate(username=username, password=password)
        if new_user:
            login(request, new_user)
            return redirect('about')
            messages.add_message(request, messages.INFO,
                'Login successful!')
        else:
            return super().post(request, *args, **kwargs)'''

class Login(LoginView):
    template_name = 'tutors/login.html'
    

    def get(self, request, *args, **kwargs):
        messages.info(request, 'Login Successful')
        return super().get(request, *args, **kwargs)

class Logout(LogoutView):
    template_name = 'tutors/logout.html'

    def get(self, request, *args, **kwargs):
        messages.success(request, 'Logout Successful')
        return super().get(request, *args, **kwargs)


'''class LogoutView(generic.RedirectView):
    url = reverse_lazy("about")

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.INFO,
                             "You have been logged out!!")
        return super().get(request, *args, **kwargs)
    
def logout(request):
    logout(request)
    return redirect('login')'''

class HelloView(generic.View):
    def get(self, request, name='World'):
        return HttpResponse(f'Hello {name}')

class GreetView(generic.View):
    greeting = 'Hello {}!'
    default_name = 'World'

    def get(self, request, **kwargs):
        name = kwargs.pop('name', self.default_name)
        return HttpResponse(self.greeting.format(name))

class SuperVillianView(GreetView):
    greeting = 'We are the future, {}. Not them. '
    default_name = 'my friend'

class ImpDateDetail(generic.DetailView):
    model = ImportantDate

class ImpDateCreate(generic.CreateView):
    model = ImportantDate
    form_class = ImportantDateForm

class ImpDateUpdate(generic.UpdateView):
    model = ImportantDate
    template_name = 'tutors/importantdate_detail.html'
    form_class = ImportantDateForm

class ImpDateDelete(generic.DeleteView):
    model = ImportantDate
    template_name = 'tutors/importantdate_form.html'
    success_url = reverse_lazy('about')

'''def page(request):
    if request.POST:
        context = {'form': form}
        form = Form_supervisor(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            login = form.cleaned_data.get('login')
            password = form.cleaned_data.get('password')
            specialization = form.cleaned_data.get('specialization')
            email = form.cleaned_data.get('email')
            new_user = User.objects.create_user(username=login, email=email, password=password)
            new_user.save()
            return reverse('about')
        else:
            return render(request, 'tutors/supervisor.html', context)
    else:
        form = Form_supervisor()
        return render(request, 'tutors/supervisor.html', context)
    if request.method == 'POST':
        if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)    
        
        
        
        
        '''


POPULAR_FROM = getattr(settings, 'VIRAL_VIDEOS_POPULAR_FROM', 500)

def viral_video_detail(request, id):
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    qs = ViralVideo.objects.annotate(
        total_impressions=\
            models.F('desktop_impressions') + models.F('mobile_impressions'),
            label=models.Case(
                models.When(total_impressions__gt=POPULAR_FROM, then=models.Value('popular')
            ), models.When(created__gt=yesterday, then=models.Value('new'),
            default=models.Value('cool'), output_field=models.CharField()
            )
    ))
    #print(qs.query)
    qs = qs.filter(pk=id)
    if request.flavour == 'mobile':
        qs.update(
            mobile_impressions=models.F('mobile_impressions') + 1
        )
    else:
        qs.update(
            desktop_impressions=models.F('desktop_impressions') + 1
        )
    video = get_object_or_404(qs)
    return render(
        request, 'lopez/viral_video.html', {'video': video}
    )

def view_404(request, exception):
    return render(request, 'tutors/404.html', {})


def view_500(request, exception=None):
    return render(request, 'tutors/404.html', {})



def response_error_handler(request, exception=None):
    return HttpResponse('Error handler content', status=403)

def permission_denied_view(request):
    raise PermissionDenied

class PublicJSON(JSONResponseMixin, generic.View):
    def get(self, request, *args, **kwargs):
        msg = Login.objects.all().values(
            'name', 'password'
        )
        return self.render_json_response(list(msg))








