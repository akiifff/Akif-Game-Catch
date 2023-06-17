from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
# Create your models here.
# class Customer(models.Model):
#     user=models.OneToOneField(User,on_delete=models.CASCADE)
#     profile_pic= models.ImageField(upload_to='profile_pic/CustomerProfilePic/',null=True,blank=True)
#     address = models.CharField(max_length=500)
#     mobile = models.CharField(max_length=10,null=False)
#     @property
#     def get_name(self):
#         return self.user.first_name+" "+self.user.last_name
#     @property
#     def get_id(self):
#         return self.user.id
#     def __str__(self):
#         return self.user.first_name



class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pic/CustomerProfilePic/', null=True, blank=True)
    address = models.CharField(max_length=500)
    mobile = models.CharField(max_length=10, null=False)
    reset_password_token = models.CharField(max_length=255, blank=True)

    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    @property
    def get_id(self):
        return self.user.id

    def __str__(self):
        return self.user.first_name

    def send_password_reset_email(self):
        token = default_token_generator.make_token(self.user)
        uid = urlsafe_base64_encode(force_bytes(self.user.id))
        reset_link = f"https://http://127.0.0.1:8000/reset-password/{uid}/{token}/"
        subject = "Password Reset"
        message = render_to_string('ecom/password_reset_email.html', {
            'reset_link': reset_link,
        })
        send_mail(subject, message, 'your-email@example.com', [self.user.email])

    @staticmethod
    def reset_password(uidb64, token, new_password):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            if default_token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                return True
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            pass
        return False

class Game(models.Model):
    name=models.CharField(max_length=40)
    game_image= models.ImageField(upload_to='game_image/',null=True,blank=True)
    price = models.PositiveIntegerField()
    description=models.CharField(max_length=4000)
    def __str__(self):
        return self.name
    
    
class CrackGame(models.Model):
    name=models.CharField(max_length=40)
    release_date= models.CharField(max_length=40,null=True)
    crack_date= models.CharField(max_length=40,null=True)
    # drm=models.CharField(max_length=40)
    # scene_grp=models.CharField(max_length=40)
    c_game_image= models.ImageField(upload_to='c_game_image/',null=True,blank=True)
    price = models.PositiveIntegerField()
    description=models.CharField(max_length=4000)
    def __str__(self):
        return self.name
    


class News(models.Model):
    title=models.CharField(max_length=40)
    news_image= models.ImageField(upload_to='news_image/',null=True,blank=True)
    posted_date= models.DateField(auto_now_add=True,null=True)
    description=models.CharField(max_length=4000)
    def __str__(self):
        return self.name
    
    
    
class Advertises(models.Model):
    title=models.CharField(max_length=40)
    adv_image= models.ImageField(upload_to='adv_image/',null=True,blank=True)
    posted_date= models.DateField(auto_now_add=True,null=True)
    description=models.CharField(max_length=4000)
    def __str__(self):
        return self.name
    
class UserAdvertises(models.Model):
    customer=models.ForeignKey('Customer', on_delete=models.CASCADE,null=True)
    title=models.CharField(max_length=40)
    u_adv_image= models.ImageField(upload_to='u_adv_image/',null=True,blank=True)
    posted_date= models.DateField(auto_now_add=True,null=True)
    description=models.CharField(max_length=4000)
    status=models.BooleanField(default=False)



class Orders(models.Model):
    STATUS =(
        ('Pending','Pending'),
        ('Order Confirmed','Order Confirmed'),
        ('Out for Delivery','Out for Delivery'),
        ('Delivered','Delivered'),
    )
    customer=models.ForeignKey('Customer', on_delete=models.CASCADE,null=True)
    game=models.ForeignKey('Game',on_delete=models.CASCADE,null=True)
    email = models.CharField(max_length=50,null=True)
    address = models.CharField(max_length=500,null=True)
    mobile = models.CharField(max_length=10,null=True)
    order_date= models.DateField(auto_now_add=True,null=True)
    status=models.CharField(max_length=50,null=True,choices=STATUS)


class Feedback(models.Model):
    name=models.CharField(max_length=40)
    feedback=models.CharField(max_length=500)
    date= models.DateField(auto_now_add=True,null=True)
    def __str__(self):
        return self.name
    
    
class Contact(models.Model):
    name=models.CharField(max_length=40)
    message=models.CharField(max_length=5000)
    date= models.DateField(auto_now_add=True,null=True)
    def __str__(self):
        return self.name
