from captcha.fields import CaptchaField
from django import forms
from .models import CustomUser, Profile


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)  # parolni input tipini password qilamiz

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'first_name',
            'last_name',
            'phone_number',
            'password',
            'email',
        ]

    def save(self, commit=True):
        user = CustomUser.objects.create_user(
            username=self.cleaned_data['username'],
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
            phone_number=self.cleaned_data.get('phone_number'),
            password=self.cleaned_data['password'],
            email=self.cleaned_data.get('email'),

        )
        return user
    # def save(self,*args,**kwargs):
    #     # user = super().save(commit=False)
    #     # user.set_password(self.cleaned_data['password'])  # parolni hash qilib saqlaymiz
    #     # if commit:
    #     #     user.save()
    #     return CustomUser.objects.create_user(*args,**kwargs)


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