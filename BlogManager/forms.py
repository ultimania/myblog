from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

class SearchForm(forms.Form):
    search_words = forms.CharField(
        initial='',
        label='記事検索',
        required = False,
        widget=forms.TextInput(
            attrs={'placeholder':'キーワード検索', 'class':'form-control'}
        )
    )

