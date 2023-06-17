from django import forms
from django.contrib.auth.models import User
from . import models


class CustomerUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password','email']
        widgets = {
        'password': forms.PasswordInput()
        }
        
class CustomerForm(forms.ModelForm):
    class Meta:
        model=models.Customer
        fields=['address','mobile','profile_pic']
        
class UserAdvertisesForm(forms.ModelForm):
    class Meta:
        model=models.UserAdvertises
        fields=['title','description','u_adv_image']

class GameForm(forms.ModelForm):
    class Meta:
        model=models.Game
        fields=['name','price','description','game_image']
        

class CrackGameForm(forms.ModelForm):
    class Meta:
        model=models.CrackGame
        fields=['name','price','description','c_game_image','release_date','crack_date']
        
       
class NewsForm(forms.ModelForm):
    class Meta:
        model=models.News
        fields=['title','description','news_image']
        
        
class AdvertisesForm(forms.ModelForm):
    class Meta:
        model=models.Advertises
        fields=['title','description','adv_image']

#address of shipment
class AddressForm(forms.Form):
    Email = forms.EmailField()
    Mobile= forms.IntegerField()
    Address = forms.CharField(max_length=500)

class FeedbackForm(forms.ModelForm):
    class Meta:
        model=models.Feedback
        fields=['name','feedback']
        
        
class ContForm(forms.ModelForm):
    class Meta:
        model=models.Contact
        fields=['name','message']

#for updating status of order
class OrderForm(forms.ModelForm):
    class Meta:
        model=models.Orders
        fields=['status']

#for contact us page
class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label='Email')