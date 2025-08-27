from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import CustomUser, EstablishmentOwner, ArtistEntrepreneur

class CustomUserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True, label="Nombre")
    last_name = forms.CharField(max_length=30, required=True, label="Apellido")
    phone = forms.CharField(max_length=20, required=False, label="Teléfono")
    user_type = forms.ChoiceField(
        choices=CustomUser.USER_TYPE_CHOICES,
        widget=forms.RadioSelect,
        label="¿Cómo te quieres registrar?"
    )
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'phone', 'user_type', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Nombre de Usuario"
        self.fields['email'].label = "Correo Electrónico"
        self.fields['password1'].label = "Contraseña"
        self.fields['password2'].label = "Confirmar Contraseña"
        
        # Añadir clases CSS
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        
        self.fields['user_type'].widget.attrs['class'] = 'form-check-input'

class EstablishmentOwnerForm(forms.ModelForm):
    class Meta:
        model = EstablishmentOwner
        fields = ['business_name', 'business_type', 'address', 'capacity', 'description', 'cuit_cuil']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class ArtistEntrepreneurForm(forms.ModelForm):
    class Meta:
        model = ArtistEntrepreneur
        fields = ['stage_name', 'category', 'bio', 'experience_years', 'portfolio_url', 'instagram', 'facebook']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class CustomLoginForm(forms.Form):
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuario o Email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
    )
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if username and password:
            self.user_cache = authenticate(username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError("Usuario o contraseña incorrectos.")
            elif not self.user_cache.is_active:
                raise forms.ValidationError("Esta cuenta está inactiva.")
        
        return self.cleaned_data
    
    def get_user(self):
        return getattr(self, 'user_cache', None)