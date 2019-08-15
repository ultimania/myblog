from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm ):
    """ログインフォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'login-form-control'
            field.widget.attrs['placeholder'] = field.label 
            field.widget.attrs['onkeyup'] = "this.setAttribute('value', this.value);"
            field.widget.attrs['value'] = ""
