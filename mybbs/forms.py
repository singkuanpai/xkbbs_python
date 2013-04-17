#-*- coding:utf-8 -*-
from django import newforms as forms
import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

class ReplyPostForm(forms.Form):
    username=forms.CharField(label="username",max_length=30)
    content=forms.TextField()
    tid=forms.IntegerField(widget=forms.HiddenInput)

    def clean_username(self):
        username=self.clean_data['username']
        if not re.search(r'^\w+$',username):
            raise forms.ValidationError('The username only include character,number,underline')
        if len(username)<3:
            raise forms.ValidationError('The username's lenght must more than 3!')
 
    def clean_tid(self):
        try:
            threads.objects.get(id=tid)
        except ObjectDoesNotExist:
            return tid
        raise forms.ValidationError('it is ok!')

