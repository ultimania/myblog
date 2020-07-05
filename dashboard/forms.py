# from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
)
from blogs.models import TopicsTr
from django.contrib.auth import get_user_model

User = get_user_model()

class SearchForm(forms.Form):
    """SearchForm
    
        検索用フォーム

    Attributes:
        search_form (django.forms.CharField): 検索フォーム部品

    """

    search_form = forms.CharField(
        initial='',
        label='記事検索',
        required = False,
        widget=forms.TextInput(
            attrs={'placeholder':'Search...', 'class':'form-control'}
        )
    )


class SigninForm(AuthenticationForm):
    """SigninForm
    
        サインイン用フォーム

    Attributes:
        username (django.forms.EmailField): ID入力フォーム

    """

    def __init__(self, *args, **kwargs):
        """__init__メソッド

        Args:
            none

        Returns:
            none
        
        Raises:
            none

        Vields:
            none
        
        Examples:
            none

        Note:
            ログイン用フォーム部品のセットアップ
            * Email
            * Password

        """
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label 
            field.widget.attrs['onkeyup'] = "this.setAttribute('value', this.value);"
            field.widget.attrs['value'] = ""
            field.label = ''


class SignupForm(UserCreationForm):
    """SignupForm
    
        サインアップ用フォーム

    Attributes:
        email (django.forms.EmailField): ID入力フォーム

    """

    class Meta:
        model = User
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        """__init__メソッド

        Args:
            none

        Returns:
            none
        
        Raises:
            none

        Vields:
            none
        
        Examples:
            none

        Note:
            ログイン用フォーム部品のセットアップ
            * Email
            * Password

        """
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label 
            field.widget.attrs['onkeyup'] = "this.setAttribute('value', this.value);"
            field.widget.attrs['value'] = ""
            field.label = ''

    def clean_email(self):
        email = self.cleaned_data['email']
        User.objects.filter(email=email, is_active=False).delete()
        return email


class TopicForm(forms.ModelForm):

    class Meta:
        model = TopicsTr
        fields = ("title","text",)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label 
            field.widget.attrs['onkeyup'] = "this.setAttribute('value', this.value);"
            field.widget.attrs['value'] = ""
            field.label = ''
        # self.fields['text'].widget.attrs['id'] = "tinymce_basic"