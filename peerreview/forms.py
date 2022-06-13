from django import forms
from django.contrib.auth.models import User
from .models import Projects, Rating, UserProfile

class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('user_name','bio','image')

class SubmitProjectForm(forms.ModelForm):
    technologies=forms.CharField(label='technologies',widget=forms.TextInput(attrs={'placeholder': 'technologies with ,'}))
                                
    class Meta:
        model = Projects
        fields = ('name','image', 'description','link','technologies')
        
class RateForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields=['design','content','usability'] 
        
    