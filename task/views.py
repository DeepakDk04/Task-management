from django.shortcuts import render, redirect

from account.models import Profile
from .models import Task
from .forms import TaskCreateForm, TaskUpdateForm

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone

# Create your views here.


@login_required(login_url='acc-login')
def home(request):
    '''
    Home Page View
    '''
    profile = Profile.objects.get(user=request.user)
    taskCount = request.user.profile.task_set.count()

    delta = timezone.now() - request.user.last_login
    sec = delta.seconds
    daysAgo = delta.days
    hoursAgo = (sec // 60) // 60

    context = {"profile": str(profile), "taskCount": taskCount,
               "daysAgo": daysAgo, "hoursAgo": hoursAgo}

    return render(request, "home.html", context)


@login_required(login_url='acc-login')
def taskViewAll(request):
    '''
    User views His Tasks
    '''
    # user = Profile.objects.get(user=request.user)
    # tasks = Task.objects.filter(owner=user)
    tasks = request.user.profile.task_set.all()
    context = {"tasks": tasks}
    return render(request, "Task/taskview.html", context)


@login_required(login_url='acc-login')
def taskView(request, task_id):
    '''
    User views the specific task using task id
    '''

    # user = Profile.objects.get(user=request.user)
    # tasks = Task.objects.filter(owner=user)
    # task = tasks.get(id=task_id)

    task = request.user.profile.task_set.get(id=task_id)
    context = {"task": task}
    return render(request, "Task/task.html", context)


@login_required(login_url='acc-login')
def taskCreate(request):
    '''
    user create his tasks
    '''
    if request.method == 'POST':

        form = TaskCreateForm(request.POST)

        if form.is_valid():
            taskName = form.cleaned_data['name']
            taskDone = form.cleaned_data['done']
            user = Profile.objects.get(user=request.user)

            task, created = Task.objects.get_or_create(
                owner=user, name=taskName, done=taskDone)

            if created:
                task.save()
                messages.success(request, 'Task Created...')

            else:
                messages.warning(request, 'Already Exists')

            return redirect('tasks-view')
        else:
            messages.error(request, 'Form is Invalid')

    taskForm = TaskCreateForm()

    context = {'taskForm': taskForm}

    return render(request, "Task/taskCreate.html", context)


@login_required(login_url='acc-login')
def taskDelete(request, task_id):
    '''
    user delete his task using task id
    '''

    # user = Profile.objects.get(user=request.user)
    # tasks = Task.objects.filter(owner=user)
    # task = tasks.get(id=task_id)
    task = request.user.profile.task_set.get(id=task_id)

    context = {'task': task}

    if request.method == 'POST':
        try:
            task.delete()
            messages.success(request, 'Task Deleted...')
            print("task deleted")
            return redirect('tasks-view')
        except Exception as e:
            messages.error(request, "task is not deleted")

    return render(request, "Task/taskDelete.html", context)


@login_required(login_url='acc-login')
def taskEdit(request, task_id):
    '''
    user edit his task using task id
    '''
    # user = Profile.objects.get(user=request.user)
    # tasks = Task.objects.filter(owner=user)
    # task = tasks.get(id=task_id)

    task = request.user.profile.task_set.get(id=task_id)
    taskForm = TaskUpdateForm(instance=task)

    if request.method == 'POST':

        taskForm = TaskUpdateForm(request.POST, instance=task)

        if taskForm.is_valid():
            taskForm.save()
            messages.success(request, 'Task Updated...')
            return redirect('tasks-view')
        else:

            messages.error(request, "Update can't be done It is invalid")

    context = {'taskForm': taskForm, 'task_id': task_id}

    return render(request, "Task/taskEdit.html", context)


def inValidURL(request):
    '''
    whenever Invalid url hits, the custom error page will displayed
    '''
    return render(request, "error404.html", {})


def devpCont(request):
    '''
    The Developer Detail Section
    '''
    email = 'deepaks@tce.edu'
    phone = '+91-***** *****'
    place = 'TCE-Madurai'
    context = {'email': email, 'phone': phone, 'place': place}
    return render(request, 'contact.html', context)
