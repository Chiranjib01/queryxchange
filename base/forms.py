from django.forms import ModelForm,CharField
from django.contrib.auth.forms import UserCreationForm
from .models import Question,User,Answer
from ckeditor.widgets import CKEditorWidget

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model=User
        fields=['name','username','email','password1','password2']

class QuestionForm(ModelForm):
    query=CharField(widget=CKEditorWidget())
    class Meta:
        model=Question
        fields='__all__'
        exclude=['host','participants']

class AnswerForm(ModelForm):
    body=CharField(widget=CKEditorWidget())
    class Meta:
        model=Answer
        fields=['body']

class UserForm(ModelForm):
    class Meta:
        model=User
        fields=['avatar','name','username','email','bio']