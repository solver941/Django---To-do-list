from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Item
import datetime
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import login
from django.contrib import auth
from django.utils import timezone
from .forms import UserLoginForm, UserSignUpForm

def index(request):
    return render(request, "app/index.html")

def add_item(request):
    #return HttpResponse("Add item")
    if request.method == "POST":
        item_name = request.POST.get("item")
        due_date = request.POST.get("due_date")
        #due_date_time = timezone.make_aware(due_date, timezone.get_current_timezone()) #adds timezone for time zone support
        print(due_date)
        foo_instance = Item.objects.create(user=request.user, question_text=item_name, due_date=due_date, pub_date=timezone.now())
        foo_instance.user = request.user
        messages.add_message(request, messages.SUCCESS, "Váš úkol byl úspěšně přidán.")
        return redirect('app:to do list')
    else:
        messages.add_message(request, messages.error, "Error")
        return redirect('app:logged_in_page')

def login(request):
    print("login function")
    form = UserLoginForm()
    return render(request, "app/login.html", {"form": form})

def login_method(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        print(request.user)
        if user is not None:
            #login(request, user)
            auth.login(request, user)
            messages.success(request, "Úspěšné přihlášení k účtu.")
            return redirect('app:logged_in_page')
        else:
            messages.error(request, 'Your username or password is incorrect.')
            return redirect("app:login")
    else:
        form = AuthenticationForm()
        return render(request, 'app/login.html', {"form": form})

@login_required
def logged_in(request):
    print("logged in function")
    return render(request, 'app/logged_in_page.html')


def register(request):
    form = UserSignUpForm()
    return render(request, "app/registration.html", { "form": form})

def register_method(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        print("post")
        if form.is_valid():
            print("valid")
            form.save()
            messages.success(request, 'Úspěšná registrace. Nyní se přihlaste ke svému účtu. ')
            return redirect('app:logged_in_page')
        else:
            render(request, 'app/registration.html')
    else:
        form = UserCreationForm()
    return render(request, 'app/registration.html', {"form": form})

def logged_out(request):
    logout(request)
    messages.success(request, 'Odlhlášení proběhlo úspěšně ')
    return redirect("app:index")

def to_do_list(request):
    user = request.user
    user_items = Item.objects.filter(user=user)
    return render(request, 'app/to_do_list.html', {"user_items": user_items})

def completed(request, id):
    item = get_object_or_404(Item, id=id)
    user = request.user
    user_items = Item.objects.filter(user=user)
    if request.user == item.user:
        item.delete()
        messages.success(request, 'Úspěšně přidáno do hotových úkolů')
        return redirect('app:to do list')
        #return render(request, 'app/to_do_list.html', {"user_items": user_items})
    else:
        messages.error(request, 'Error deleting item.')
        return render(request, 'app/to_do_list.html', {"user_items": user_items})

def edit(request, id):
    item = get_object_or_404(Item, id=id)
    print(item.due_date)
    user = request.user
    user_items = Item.objects.filter(user=user)
    return render(request, 'app/edit.html', {"user_item":item})

def edit_item(request, id):
    user = request.user
    user_items = Item.objects.filter(user=user)
    item = get_object_or_404(Item, id=id)
    if request.method == "POST":
        item.question_text = request.POST.get("item")
        item.due_date = request.POST.get("due_date")
        item.save()
        messages.add_message(request, messages.SUCCESS, "Váš úkol byl úspěšně upraven")
        return redirect('app:to do list')
    else:
        messages.add_message(request, messages.error, "Error")
        return redirect('app:logged_in_page')
