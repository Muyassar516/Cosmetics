from captcha.fields import CaptchaField
from django.contrib.auth.forms import AuthenticationForm

from .models import CustomUser, Profile, RoleChoice
from django import forms

class UserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Parol",
        help_text="Kamida 8 ta belgi bo'lishi kerak"
    )
    role = forms.ChoiceField(
        choices=[(RoleChoice.READER, 'Xaridor'), (RoleChoice.PUBLISHER, 'Sotuvchi')],
        widget=forms.RadioSelect,
        label="Siz kim sifatida ro‘yxatdan o‘tasiz?"
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'phone_number', 'email', 'password', 'role']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nickname', 'bio', 'email', 'image']


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Foydalanuvchi nomi",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Foydalanuvchi nomi'
        })
    )
    password = forms.CharField(
        label="Parol",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Parol'
        })
    )
    captcha = CaptchaField(label="Rasmdagi so‘zni yozing")

class LoginForm(forms.Form):
    username = forms.CharField(max_length=40)
    password = forms.CharField(widget=forms.PasswordInput, max_length=50)
    captcha = CaptchaField()
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user', 'email', 'bio']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@gmail.com'):
            raise forms.ValidationError("Faqat @gmail.com email manzillariga ruxsat bor!")
        return email

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nickname', 'image', 'bio']
        labels = {
            'nickname': "Nomingiz",
            'image': "Profil rasmi",
            'bio': "Bio (o'zingiz haqida qisqacha)"
        }

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'phone_number']
        labels = {
            'email': "Email manzilingiz",
            'phone_number': "Telefon raqamingiz"
        }

#
# class UserForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)
#     role = forms.ChoiceField(
#         choices=[(RoleChoice.READER, 'Xaridor'), (RoleChoice.PUBLISHER, 'Sotuvchi')],
#         initial=RoleChoice.READER,
#         widget=forms.RadioSelect
#     )
#
#     class Meta:
#         model = CustomUser
#         fields = [
#             'username',
#             'first_name',
#             'last_name',
#             'phone_number',
#             'password',
#             'email',
#             'role',
#         ]
#
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data['password'])
#         if commit:
#             user.save()
#         return user
