from django import forms
from .models import *
from administrator.models import *
from enrollee.models import *

class EnrolleeRegistrationForm(forms.ModelForm):

	class Meta:
		model = Enrollee
		fields = ('user', 'address', 'level')

# class QuestionForm(forms.ModelForm):

# 	class Meta():
# 		model = Question
# 		fields = ('__all__')