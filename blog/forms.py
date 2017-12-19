from django import forms
from django.forms import IntegerField,Textarea,CharField,DateField,ChoiceField


# 发表，编辑表单
class PublishForm(forms.Form):
    aid = forms.IntegerField()
    title = forms.CharField(max_length=100)
    content = forms.CharField(widget=forms.Textarea)