from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout as auth_logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomPasswordChangeForm


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('website:dashboard')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'customusers/login.html', {'form': form})




def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('website:dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'customusers/register.html', {'form': form})




@login_required
def password_change_view(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password was successfully updated!")
            return redirect('password_change_done')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'customusers/password_change.html', {'form': form})





# Logout view
@login_required
def logout_view(request):
    auth_logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')









# Password change done view
@login_required
def password_change_done_view(request):
    return render(request, 'customusers/password_change_done.html')