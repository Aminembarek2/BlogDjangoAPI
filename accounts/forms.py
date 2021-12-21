from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
    )
from accounts.models import User

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            user = User.objects.filter(username=username)
            if user.exists() and user.count() == 1:
                user_obj=user.first()
            else:
                raise forms.ValidationError("The username is not valid.")
            if user_obj:
                if not user_obj.check_password(password):
                    raise forms.ValidationError("Incorrect passsword")
                if not user_obj.is_active:
                    raise forms.ValidationError("This user is not longer active.")
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField(label='Email address')
    re_password = forms.CharField(label='Confirm Password',widget=forms.PasswordInput)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password'
        ]
    def clean_re_password(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('re_password')
        if password != re_password:
            raise forms.ValidationError("Emails must match")
        # username_qs = User.objects.filter(username=username)
        # if username_qs.exists():
        #     raise forms.ValidationError("This email has already been registered")
        return email