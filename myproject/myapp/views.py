from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import ProblemForm
from .models import Problem


def prehome(request):
    return render(request, "prehome/prehome.html", {"prehome": prehome})


def create_problem(request):
    if request.method == 'POST':
        form = ProblemForm(request.POST)
        if form.is_valid():
            problem = form.save(commit=False)
            reception_group = Group.objects.get(name='Reception')
            reception_users = reception_group.user_set.all()
            if reception_users.exists():
                problem.assigned_user = reception_users[0] 
            problem.save()
            return redirect('problem_list')
    else:
        form = ProblemForm()
    return render(request, 'create_problem.html', {'form': form})
    

def problem_list(request):
    user = request.user
    if user.groups.filter(name='Reception').exists():
        problems = Problem.objects.all()
    else:
        problems = Problem.objects.filter(assigned_user=user)
    
    return render(request, 'problem_list.html', {'problems': problems, 'is_tester': user.groups.filter(name='Tester').exists()})

def update_problem_status(problem, new_status, user):
    if new_status == 'resolved':
        problem.resolved_user = problem.assigned_user
        tester_group = Group.objects.get(name='Tester')
        testers = tester_group.user_set.all()
        if testers.exists():
            problem.assigned_user = testers[0]  
    problem.resolved = new_status
    problem.save()

def profile_view(request):
    user = request.user
    is_tester = user.groups.filter(name='Tester').exists()
    return render(request, 'login\profile.html', {'user': user, 'is_tester': is_tester})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('problem_list')
        else:
            return render(request, 'login\login.html', {'error_message': 'Invalid login'})
    else:
        return render(request, 'login\login.html')

def logout_view(request):
    logout(request)
    return redirect('prehome')

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'login\signup.html'