# from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import TopicsTr, MediaTr

class UploadForm(forms.ModelForm):

    class Meta:
        model = MediaTr
        fields = ('file',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['form'] = "upload_form"


class SearchForm(forms.Form):
    search_words = forms.CharField(
        initial='',
        label='記事検索',
        required = False,
        widget=forms.TextInput(
            attrs={'placeholder':'キーワード検索', 'class':'form-control'}
        )
    )


class PostForm(forms.ModelForm):

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
