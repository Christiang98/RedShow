from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .forms import CustomUserRegistrationForm, EstablishmentOwnerForm, ArtistEntrepreneurForm, CustomLoginForm
from .models import CustomUser

class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'accounts/login.html'
    
    def get_success_url(self):
        return reverse_lazy('dashboard')

def register_view(request):
    if request.method == 'POST':
        user_form = CustomUserRegistrationForm(request.POST)
        
        if user_form.is_valid():
            user = user_form.save()
            user_type = user_form.cleaned_data['user_type']
            
            if user_type == 'owner':
                return redirect('complete_owner_profile')
            else:
                return redirect('complete_artist_profile')
    else:
        user_form = CustomUserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': user_form})

@login_required
def complete_owner_profile(request):
    if request.user.user_type != 'owner':
        messages.error(request, 'No tienes permisos para acceder a esta página.')
        return redirect('dashboard')
    
    if hasattr(request.user, 'owner_profile'):
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = EstablishmentOwnerForm(request.POST)
        if form.is_valid():
            owner_profile = form.save(commit=False)
            owner_profile.user = request.user
            owner_profile.save()
            messages.success(request, '¡Perfil completado exitosamente!')
            return redirect('dashboard')
    else:
        form = EstablishmentOwnerForm()
    
    return render(request, 'accounts/complete_owner_profile.html', {'form': form})

@login_required
def complete_artist_profile(request):
    if request.user.user_type != 'artist':
        messages.error(request, 'No tienes permisos para acceder a esta página.')
        return redirect('dashboard')
    
    if hasattr(request.user, 'artist_profile'):
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = ArtistEntrepreneurForm(request.POST)
        if form.is_valid():
            artist_profile = form.save(commit=False)
            artist_profile.user = request.user
            artist_profile.save()
            messages.success(request, '¡Perfil completado exitosamente!')
            return redirect('dashboard')
    else:
        form = ArtistEntrepreneurForm()
    
    return render(request, 'accounts/complete_artist_profile.html', {'form': form})