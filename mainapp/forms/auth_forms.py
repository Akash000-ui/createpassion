from django import forms


class UserRegistrationForm(forms.Form):
    first_name  = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'First Name'
    }))
    last_name   = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Last Name'
    }))
    email       = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'Email Address'
    }))
    mobile      = forms.CharField(max_length=15, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Mobile Number'
    }))
    password    = forms.CharField(min_length=8, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Password'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Confirm Password'
    }))

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile', '').strip()
        if not mobile.isdigit():
            raise forms.ValidationError('Mobile number must contain only digits.')
        if len(mobile) != 10:
            raise forms.ValidationError('Mobile number must be exactly 10 digits.')
        return mobile

    def clean(self):
        cleaned = super().clean()
        password = cleaned.get('password')
        confirm  = cleaned.get('confirm_password')
        if password and confirm and password != confirm:
            raise forms.ValidationError('Passwords do not match.')
        return cleaned


class UserLoginForm(forms.Form):
    identifier = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Email or Member ID (e.g. CP35858)', 'autofocus': True
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Password'
    }))


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'Enter your registered email'
    }))


class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(min_length=8, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'New Password'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Confirm New Password'
    }))

    def clean(self):
        cleaned = super().clean()
        pw  = cleaned.get('new_password')
        cpw = cleaned.get('confirm_password')
        if pw and cpw and pw != cpw:
            raise forms.ValidationError('Passwords do not match.')
        return cleaned
