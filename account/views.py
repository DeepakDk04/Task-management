from django.http.response import HttpResponseBadRequest
from task.models import Task
from django.shortcuts import render, redirect


from django.contrib import messages
from .forms import CreateUserForm, updateProfile
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required
from .decorators import unauthendicated_user, allowed_users, admin_only


from .models import Profile
from django.contrib.auth.models import User
# Create your views here.


def home(request):

    context = {}
    return render(request, "home.html", context)


@unauthendicated_user
def register(request):
    '''
    Create an account for user
    '''
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')

            messages.success(
                request, 'Account created Succesfully for ' + username)

            return redirect('acc-login')

    context = {'form': form}
    return render(request, "Account/register.html", context)


@unauthendicated_user
def loginUser(request):
    '''
    Let the user logged in
    '''
    context = {}

    if request.method == 'POST':
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)

        if username and password:

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')

            messages.info(request, 'Username or Password are Incorrect...')

    return render(request, "Account/login.html", context)


def logoutUser(request):
    '''
    Let the user logged out
    '''
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "You are logged out...")
        return redirect('acc-login')

    messages.info(request, "Can't logout. You are not looged in")
    return HttpResponseBadRequest("You are not logged in to logout")


def usernameValidation(username):
    '''
    Custom Utility Function that validate username
    '''
    msg = ''

    if len(username) < 4:
        msg += '"Username" must be atleast 4 Characters '
        return (False, msg)

    upper, num, spl, splCh = False, False, False, ['_', '@', '.']
    for letter in str(username):
        if letter.isnumeric():
            num = True
        elif letter.isupper():
            upper = True
        elif letter in splCh:
            spl = True

    if not num or not upper or not spl:
        msg = "'Username' must include atleast One Number and One Uppercase Letter and One Special Character from [ _ and . and @ ] "

    if msg:
        return (False, msg)
    else:
        return (True, msg)


def profileUpdateValidation(req):
    '''
    Custom function that validates the Profile Updation request
    '''
    msg = ''
    username = req.POST.get('username', '')
    email = req.POST.get('email', '')

    if not username:
        msg += "Username can't be Empty "
        return (False, msg)
    if not email:
        msg += "Please enter 'Email' "
        return (False, msg)

    oldUserName = req.user.username
    oldUserEmail = req.user.email

    if oldUserName == username and oldUserEmail == email:
        # both username, email is not changed, no need validations
        return (True, msg)

    if oldUserName == username and oldUserEmail != email:
        # username is not changed, email is changed
        if User.objects.filter(email=email).exists():
            msg += str(email) + ' is associated with another account...'
            return (False, msg)

    if oldUserName != username and oldUserEmail == email:
        # username is changed , email is not changed

        valid, msg = usernameValidation(username)

        if valid:
            if User.objects.filter(username=username).exists():
                msg += 'The Username ' + str(username) + ' is not available...'
                return (False, msg)
            else:
                return (True, msg)
        else:
            return (False, msg)

    if oldUserName != username and oldUserEmail != email:
        # username is changed , email is changed

        valid, msg = usernameValidation(username)

        if valid:
            if User.objects.filter(username=username).exists():
                msg += 'The Username ' + str(username) + ' is not available...'
                return (False, msg)
            else:
                if User.objects.filter(email=email).exists():
                    msg += str(email) + \
                        ' is associated with another account...'
                    return (False, msg)
                else:
                    return (True, msg)

        else:
            return (False, msg)


def isProfileChanged(req):
    '''
    Checks whether the request is made for any changes,
    or unnesscessary request to update same information
    '''
    username = req.POST.get('username', '')
    email = req.POST.get('email', '')
    first_name = req.POST.get('first_name', '')
    last_name = req.POST.get('last_name', '')

    user = req.user

    if user.username == username:
        if user.email == email:
            if user.first_name == first_name:
                if user.last_name == last_name:
                    return False

    return True


@login_required(login_url='acc-login')
@allowed_users(allowed_roles=['user-group', 'admin-group'])
def profileSetting(request):
    '''
    let the user update his profile data
    '''
    form = updateProfile(instance=request.user)

    if request.method == "POST":

        if isProfileChanged(request):
            valid, msg = profileUpdateValidation(request)
            if not valid:
                messages.error(request, msg)
            else:
                form = updateProfile(request.POST, instance=request.user)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Profile Updated...')
                else:
                    messages.error(request, "Can't Update Profile")

    context = {'form': form}
    return render(request, "Account/profilesetting.html", context)


@login_required(login_url='acc-login')
# @allowed_users(allowed_roles=['admin-group'])
@admin_only
def usersStat(request):
    '''
    generate the user stats and user profile details from the database.
    '''

    allProfile = Profile.objects.all()
    profilesCount = allProfile.count()
    tasksCount = Task.objects.count()
    lastProfile = Profile.objects.last().user.username
    latestTask = Task.objects.last().createdOn

    context = {"allProfile": allProfile,
               "profilesCount": profilesCount, "tasksCount": tasksCount,
               "lastProfile": lastProfile, "latestTask": latestTask}

    return render(request, "Account/userStat.html", context)


@login_required(login_url='acc-login')
@admin_only
def userDetail(request, user_id):
    '''
    view the users details from the given user id
    '''

    profile = Profile.objects.get(id=user_id)
    tasks_owned = profile.task_set.count()
    context = {"profile": profile, "tasks_owned": tasks_owned}

    return render(request, "Account/userDetail.html", context)
