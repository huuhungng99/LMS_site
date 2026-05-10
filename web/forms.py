from django import forms
from django.contrib.auth.models import User
from .models import *

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['profile_pic', 'address', 'mobile', 'enrollment_number', 'date_of_birth', 'gender']  # Không bao gồm user

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['description', 'file']  # Các trường bạn muốn bao gồm trong form

    def __init__(self, *args, **kwargs):
        super(MaterialForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs.update({'class': 'description-field'})

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['quiz', 'question_text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer']