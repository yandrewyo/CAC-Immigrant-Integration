from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.conf import settings
from django.http import JsonResponse
from .utils import get_response
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import UserRegistrationForm,UserProfileForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.urls import reverse

def chat(request):
    filename = request.session.get('module_file_name')
    if not filename:
        return JsonResponse({"error": "No filename provided in session"}, status=400)
    if request.method == "POST":
        user_message = request.POST.get('message')
        if not user_message:
            return JsonResponse({"error": "No message provided"}, status=400)

        try:
            response = get_response(user_message,filename)
            return JsonResponse({"message": response})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)

# Create your views here.
@login_required
def index(request):
    return render(request, "index.html")


@login_required
def timeline(request):
    return render(request, "timeline.html")



@login_required
def create_profile(request):
    if UserProfile.objects.filter(user=request.user).exists():
        return JsonResponse({'success': False, 'redirect_url': reverse('profile_view')})

    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            return JsonResponse({'success': True, 'message': 'Profile created successfully!', 'redirect_url': reverse('index')})
        else:
            return JsonResponse({'success': False, 'message': 'Form is not valid.'})
    else:
        form = UserProfileForm()

    return render(request, 'profile_form.html', {'form': form})

@login_required
def profile_view(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return redirect('create_profile')  # Redirect to profile creation if no profile exists

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Profile updated successfully!', 'redirect_url': reverse('index')})
        else:
            return JsonResponse({'success': False, 'message': 'Form is not valid.'})
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'profile_form.html', {'form': form})

# @login_required
# def create_profile(request):
#     if UserProfile.objects.filter(user=request.user).exists():
#         return redirect('profile_view')  # Redirect to profile view if profile already exists

#     if request.method == 'POST':
#         form = UserProfileForm(request.POST)
#         if form.is_valid():
#             user_profile = form.save(commit=False)
#             user_profile.user = request.user
#             user_profile.save()
#             messages.success(request, 'Profile created successfully!')
#             return redirect('index')
#     else:
#         form = UserProfileForm()

#     return render(request, 'profile_form.html', {'form': form})

# @login_required
# def profile_view(request):
#     try:
#         user_profile = UserProfile.objects.get(user=request.user)
#     except UserProfile.DoesNotExist:
#         return redirect('create_profile')  # Redirect to profile creation if no profile exists

#     if request.method == 'POST':
#         form = UserProfileForm(request.POST, instance=user_profile)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Profile updated successfully!')
#             return redirect('profile_view')  # Redirect to the same page after updating
#     else:
#         form = UserProfileForm(instance=user_profile)

#     return render(request, 'profile_form.html', {'form': form})

def preview(request):
    context = {}
    if "module" in request.GET:
        context["module"] = request.GET.get("module")
        context["module_title"] = " ".join(request.GET.get("module").split("-")).title()
    return render(request, "preview.html", context)


def module(request):
    context = {}
    if "module" in request.GET:
        context["module"] = request.GET.get("module")
        context["module_title"] = " ".join(request.GET.get("module").split("-")).title()
        context["module_file_name"] = context["module"] + ".pdf"
        request.session['module_file_name'] = context["module_file_name"]

    return render(request, "module.html", context)

def register_new(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            
            user = authenticate(username=new_user.username, password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('create_profile')
            else:
                # Handle authentication failure if necessary
                pass
    else:
        form = UserRegistrationForm()
        
    return render(request, 'register_new.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['uname']
        password = request.POST['psw']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # Redirect to the main app page
        else:
            return HttpResponse("Invalid login credentials.")  # Handle invalid login
    return render(request, 'login.html')  # Display the login page


# def register(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             new_user = form.save(commit=False)
#             new_user.set_password(form.cleaned_data['password'])
#             new_user.save()
#             user = authenticate(username=new_user.username, password=form.cleaned_data['password'])
#             login(request, user)
#             return redirect('index')
#     else:
#         form = UserRegistrationForm()
#     return render(request, 'register.html', {'form': form})