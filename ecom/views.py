from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.http import HttpResponseRedirect,HttpResponse
from django.core.mail import send_mail
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages
from django.conf import settings
from django.shortcuts import get_object_or_404
from ecom.models import Customer
from django.contrib.auth.forms import SetPasswordForm
# //password
from django.contrib.auth import get_user_model

from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.tokens import default_token_generator
# //ss
from django.contrib.auth.forms import PasswordResetForm

from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy

from django.contrib.sites.shortcuts import get_current_site

def allgames(request):
    Games=models.Game.objects.all()
    Advertises=models.Advertises.objects.all()
    News=models.News.objects.all()
    if 'Game_ids' in request.COOKIES:
        Game_ids = request.COOKIES['Game_ids']
        counter=Game_ids.split('|')
        Game_count_in_cart=len(set(counter))
    else:
        Game_count_in_cart=0
    
        # return HttpResponseRedirect('afterlogin')
    return render(request,'gamepages/index.html',{'Games':Games,'News':News,'Advertises':Advertises,'Game_count_in_cart':Game_count_in_cart})
    
def allcrackgames(request):
    CrackGames=models.CrackGame.objects.all()
    Advertises=models.Advertises.objects.all()
    News=models.News.objects.all()
    if 'CrackGame_ids' in request.COOKIES:
        CrackGame_ids = request.COOKIES['CrackGame_ids']
        counter=CrackGame_ids.split('|')
        CrackGame_count_in_cart=len(set(counter))
    else:
        CrackGame_count_in_cart=0
    
        # return HttpResponseRedirect('afterlogin')
    return render(request,'gamepages/index3.html',{'CrackGames':CrackGames,'News':News,'Advertises':Advertises,'CrackGame_count_in_cart':CrackGame_count_in_cart})
    



def detail_game_view(request, pk):
    game = models.Game.objects.get(id=pk)
    advertises=models.Advertises.objects.all()
    context = {
        'game': game,
        'advertises':advertises
    }
    return render(request, 'gamepages/anime-details.html', context)


def detail_crack_game_view(request, pk):
    crackgame = models.CrackGame.objects.get(id=pk)
    advertises=models.Advertises.objects.all()
    context = {
        'crackgame': crackgame,
        'advertises':advertises
    }
    return render(request, 'gamepages/anime-details2.html', context)
# def detail_game_view(request,pk):
#     Games=models.Game.objects.get(id=pk)
#     if 'Game_ids' in request.COOKIES:
#         Game_ids = request.COOKIES['Game_ids']
#         counter=Game_ids.split('|')
#         Game_count_in_cart=len(set(counter))
#     else:
#         Game_count_in_cart=0
#     if request.user.is_authenticated:
#         return HttpResponseRedirect('afterlogin')
#     return render(request,'gamepages/anime-details.html',{'Games':Games,'Game_count_in_cart':Game_count_in_cart})
    


#for showing login button for admin
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')


def customer_signup_view(request):
    userForm=forms.CustomerUserForm()
    customerForm=forms.CustomerForm()
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST)
        customerForm=forms.CustomerForm(request.POST,request.FILES)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customer=customerForm.save(commit=False)
            customer.user=user
            customer.save()
            my_customer_group = Group.objects.get_or_create(name='CUSTOMER')
            my_customer_group[0].user_set.add(user)
        return HttpResponseRedirect('customerlogin')
    return render(request,'ecom/customersignup.html',context=mydict)

#-----------for checking user iscustomer
def is_customer(user):
    return user.groups.filter(name='CUSTOMER').exists()



#---------AFTER ENTERING CREDENTIALS WE CHECK WHETHER USERNAME AND PASSWORD IS OF ADMIN,CUSTOMER
def afterlogin_view(request):
    if is_customer(request.user):
        return redirect('customer-home')
    else:
        return redirect('admin-dashboard')

#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    # for cards on dashboard
    customercount=models.Customer.objects.all().count()
    Gamecount=models.Game.objects.all().count()
    ordercount=models.Orders.objects.all().count()

    # for recent order tables
    orders=models.Orders.objects.all()
    ordered_Games=[]
    ordered_bys=[]
    for order in orders:
        ordered_Game=models.Game.objects.all().filter(id=order.game.id)
        ordered_by=models.Customer.objects.all().filter(id = order.customer.id)
        ordered_Games.append(ordered_Game)
        ordered_bys.append(ordered_by)

    mydict={
    'customercount':customercount,
    'Gamecount':Gamecount,
    'ordercount':ordercount,
    'data':zip(ordered_Games,ordered_bys,orders),
    }
    return render(request,'ecom/admin_dashboard.html',context=mydict)


# admin view customer table
@login_required(login_url='adminlogin')
def view_customer_view(request):
    customers=models.Customer.objects.all()
    return render(request,'ecom/view_customer.html',{'customers':customers})

# admin delete customer
@login_required(login_url='adminlogin')
def delete_customer_view(request,pk):
    customer=models.Customer.objects.get(id=pk)
    user=models.User.objects.get(id=customer.user_id)
    user.delete()
    customer.delete()
    return redirect('view-customer')


@login_required(login_url='adminlogin')
def update_customer_view(request,pk):
    customer=models.Customer.objects.get(id=pk)
    user=models.User.objects.get(id=customer.user_id)
    userForm=forms.CustomerUserForm(instance=user)
    customerForm=forms.CustomerForm(request.FILES,instance=customer)
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST,instance=user)
        customerForm=forms.CustomerForm(request.POST,instance=customer)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customerForm.save()
            return redirect('view-customer')
    return render(request,'ecom/admin_update_customer.html',context=mydict)

# admin view the game
@login_required(login_url='adminlogin')
def admin_Games_view(request):
    Games=models.Game.objects.all()
    return render(request,'ecom/admin_Games.html',{'Games':Games})


# admin view the game
@login_required(login_url='adminlogin')
def admin_CrackGames_view(request):
    CrackGames=models.CrackGame.objects.all()
    return render(request,'ecom/admin_CrackGames.html',{'CrackGames':CrackGames})


# admin view the news
@login_required(login_url='adminlogin')
def admin_News_view(request):
    News=models.News.objects.all()
    return render(request,'ecom/admin_News.html',{'News':News})


# @login_required(login_url='adminlogin')
def customer_News_view(request):
    News=models.News.objects.all()
    return render(request,'gamepages/blog-details.html',{'News':News})



# admin view the advertises
@login_required(login_url='adminlogin')
def admin_Advertises_view(request):
    Advertises=models.Advertises.objects.all()
    return render(request,'ecom/admin_Advertises.html',{'Advertises':Advertises})

@login_required(login_url='adminlogin')
def admin_UserAdvertises_view(request):
    Advertises=models.UserAdvertises.objects.all().filter(status=False)
    return render(request,'ecom/admin_UserAdvertises.html',{'Advertises':Advertises})



def user_UserAdvertises_view(request):
    Advertises=models.UserAdvertises.objects.all().filter(status=True)
    return render(request,'gamepages/customer_view_Advertises.html',{'Advertises':Advertises})



def user_Advertises_view(request):
    Advertises=models.Advertises.objects.all()
    return render(request,'gamepages/advertise.html',{'Advertises':Advertises})


@login_required(login_url='adminlogin')

def approve_Add_view(request,pk):
    UserAdvertises=models.UserAdvertises.objects.get(id=pk)
    UserAdvertises.status=True
    UserAdvertises.save()
    return redirect(reverse('admin-UserAdvertises'))

@login_required(login_url='adminlogin')

def reject_Add_view(request,pk):
    UserAdvertises=models.UserAdvertises.objects.get(id=pk)
    # user=models.User.objects.get(id=UserAdvertises.user_id)
    # user.delete()
    UserAdvertises.delete()
    return redirect('admin-UserAdvertises')

# admin add game by clicking on floating button
@login_required(login_url='adminlogin')
def admin_add_Game_view(request):
    GameForm=forms.GameForm()
    if request.method=='POST':
        GameForm=forms.GameForm(request.POST, request.FILES)
        if GameForm.is_valid():
            GameForm.save()
        return HttpResponseRedirect('admin-Games')
    return render(request,'ecom/admin_add_Games.html',{'GameForm':GameForm})




# admin add crack game by clicking on floating button
@login_required(login_url='adminlogin')
def admin_add_CrackGame_view(request):
    CrackGameForm=forms.CrackGameForm()
    if request.method=='POST':
        CrackGameForm=forms.CrackGameForm(request.POST, request.FILES)
        if CrackGameForm.is_valid():
            CrackGameForm.save()
        return HttpResponseRedirect('admin-CrackGames')
    return render(request,'ecom/admin_add_CrackGames.html',{'CrackGameForm':CrackGameForm})



# admin add news by clicking on floating button
@login_required(login_url='adminlogin')
def admin_add_News_view(request):
    NewsForm=forms.NewsForm()
    if request.method=='POST':
        NewsForm=forms.NewsForm(request.POST, request.FILES)
        if NewsForm.is_valid():
            NewsForm.save()
        return HttpResponseRedirect('admin-News')
    return render(request,'ecom/admin_add_News.html',{'NewsForm':NewsForm})


# admin add advertises by clicking on floating button
@login_required(login_url='adminlogin')
def admin_add_Advertises_view(request):
    AdvertisesForm=forms.AdvertisesForm()
    if request.method=='POST':
        AdvertisesForm=forms.AdvertisesForm(request.POST, request.FILES)
        if AdvertisesForm.is_valid():
            AdvertisesForm.save()
        return HttpResponseRedirect('admin-Advertises')
    return render(request,'ecom/admin_add_Advertises.html',{'AdvertisesForm':AdvertisesForm})


@login_required(login_url='customerlogin')
def customer_add_Advertises_view(request):
    UserAdvertisesForm = forms.UserAdvertisesForm()
    if request.method == 'POST':
        UserAdvertisesForm = forms.UserAdvertisesForm(request.POST, request.FILES)
        if UserAdvertisesForm.is_valid():
            user_advertisement = UserAdvertisesForm.save(commit=False)
            customer=models.Customer.objects.get(user_id=request.user.id)
            user_advertisement.customer = customer # Store the logged-in user's ID
            user_advertisement.save()
            return HttpResponseRedirect('/')
    return render(request, 'gamepages/customer_add_Advertises.html', {'UserAdvertisesForm': UserAdvertisesForm})



@login_required(login_url='adminlogin')
def delete_Game_view(request,pk):
    game=models.Game.objects.get(id=pk)
    game.delete()
    return redirect('admin-Games')


@login_required(login_url='adminlogin')
def delete_CrackGame_view(request,pk):
    crackgame=models.CrackGame.objects.get(id=pk)
    crackgame.delete()
    return redirect('admin-CrackGames')


@login_required(login_url='adminlogin')
def delete_News_view(request,pk):
    news=models.News.objects.get(id=pk)
    news.delete()
    return redirect('admin-News')


@login_required(login_url='adminlogin')
def delete_Advertises_view(request,pk):
    advertises=models.Advertises.objects.get(id=pk)
    advertises.delete()
    return redirect('admin-Advertises')


@login_required(login_url='adminlogin')
def update_Game_view(request,pk):
    game=models.Game.objects.get(id=pk)
    GameForm=forms.GameForm(instance=game)
    if request.method=='POST':
        GameForm=forms.GameForm(request.POST,request.FILES,instance=game)
        if GameForm.is_valid():
            GameForm.save()
            return redirect('admin-Games')
    return render(request,'ecom/admin_update_Game.html',{'GameForm':GameForm})



@login_required(login_url='adminlogin')
def update_CrackGame_view(request,pk):
    crackgame=models.CrackGame.objects.get(id=pk)
    CrackGameForm=forms.CrackGameForm(instance=crackgame)
    if request.method=='POST':
        CrackGameForm=forms.CrackGameForm(request.POST,request.FILES,instance=crackgame)
        if CrackGameForm.is_valid():
            CrackGameForm.save()
            return redirect('admin-CrackGames')
    return render(request,'ecom/admin_update_CrackGame.html',{'CrackGameForm':CrackGameForm})


@login_required(login_url='adminlogin')
def update_News_view(request,pk):
    news=models.News.objects.get(id=pk)
    NewsForm=forms.NewsForm(instance=news)
    if request.method=='POST':
        NewsForm=forms.NewsForm(request.POST,request.FILES,instance=news)
        if NewsForm.is_valid():
            NewsForm.save()
            return redirect('admin-News')
    return render(request,'ecom/admin_update_News.html',{'NewsForm':NewsForm})


@login_required(login_url='adminlogin')
def update_Advertises_view(request,pk):
    advertises=models.Advertises.objects.get(id=pk)
    AdvertisesForm=forms.AdvertisesForm(instance=advertises)
    if request.method=='POST':
        AdvertisesForm=forms.AdvertisesForm(request.POST,request.FILES,instance=advertises)
        if AdvertisesForm.is_valid():
            AdvertisesForm.save()
            return redirect('admin-Advertises')
    return render(request,'ecom/admin_update_Advertises.html',{'AdvertisesForm':AdvertisesForm})


@login_required(login_url='adminlogin')
def admin_view_booking_view(request):
    orders=models.Orders.objects.all()
    ordered_Games=[]
    ordered_bys=[]
    for order in orders:
        ordered_Game=models.Game.objects.all().filter(id=order.game.id)
        ordered_by=models.Customer.objects.all().filter(id = order.customer.id)
        ordered_Games.append(ordered_Game)
        ordered_bys.append(ordered_by)
    return render(request,'ecom/admin_view_booking.html',{'data':zip(ordered_Games,ordered_bys,orders)})


@login_required(login_url='adminlogin')
def delete_order_view(request,pk):
    order=models.Orders.objects.get(id=pk)
    order.delete()
    return redirect('admin-view-booking')

# for changing status of order (pending,delivered...)
@login_required(login_url='adminlogin')
def update_order_view(request,pk):
    order=models.Orders.objects.get(id=pk)
    orderForm=forms.OrderForm(instance=order)
    if request.method=='POST':
        orderForm=forms.OrderForm(request.POST,instance=order)
        if orderForm.is_valid():
            orderForm.save()
            return redirect('admin-view-booking')
    return render(request,'ecom/update_order.html',{'orderForm':orderForm})


# admin view the feedback
@login_required(login_url='adminlogin')
def view_feedback_view(request):
    feedbacks=models.Feedback.objects.all().order_by('-id')
    return render(request,'ecom/view_feedback.html',{'feedbacks':feedbacks})



#---------------------------------------------------------------------------------
#------------------------ PUBLIC CUSTOMER RELATED VIEWS START ---------------------
#---------------------------------------------------------------------------------
def search_view(request):
    # whatever user write in search box we get in query
    query = request.GET['query']
    Games=models.Game.objects.all().filter(name__icontains=query)
    if 'Game_ids' in request.COOKIES:
        Game_ids = request.COOKIES['Game_ids']
        counter=Game_ids.split('|')
        Game_count_in_cart=len(set(counter))
    else:
        Game_count_in_cart=0

    # word variable will be shown in html when user click on search button
    word="Searched Result :"

    if request.user.is_authenticated:
        return render(request,'ecom/customer_home.html',{'Games':Games,'word':word,'Game_count_in_cart':Game_count_in_cart})
    return render(request,'ecom/index.html',{'Games':Games,'word':word,'Game_count_in_cart':Game_count_in_cart})

@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def add_to_cart_view(request,pk):
    Games=models.Game.objects.all()

    #for cart counter, fetching Games ids added by customer from cookies
    if 'Game_ids' in request.COOKIES:
        Game_ids = request.COOKIES['Game_ids']
        counter=Game_ids.split('|')
        Game_count_in_cart=len(set(counter))
    else:
        Game_count_in_cart=1
    
    response = render(request, 'gamepages/index.html',{'Games':Games,'Game_count_in_cart':Game_count_in_cart})

    #adding game id to cookies
    if 'Game_ids' in request.COOKIES:
        Game_ids = request.COOKIES['Game_ids']
        if Game_ids=="":
            Game_ids=str(pk)
        else:
            Game_ids=Game_ids+"|"+str(pk)
        response.set_cookie('Game_ids', Game_ids)
    else:
        response.set_cookie('Game_ids', pk)

    game=models.Game.objects.get(id=pk)
    messages.info(request, game.name + ' added to cart successfully!')

    return response



# for checkout of cart
def cart_view(request):
    #for cart counter
    if 'Game_ids' in request.COOKIES:
        Game_ids = request.COOKIES['Game_ids']
        counter=Game_ids.split('|')
        Game_count_in_cart=len(set(counter))
    else:
        Game_count_in_cart=0

    # fetching game details from db whose id is present in cookie
    Games=None
    total=0
    if 'Game_ids' in request.COOKIES:
        Game_ids = request.COOKIES['Game_ids']
        if Game_ids != "":
            Game_id_in_cart=Game_ids.split('|')
            Games=models.Game.objects.all().filter(id__in = Game_id_in_cart)

            #for total price shown in cart
            for p in Games:
                total=total+p.price
    return render(request,'gamepages/cart.html',{'Games':Games,'total':total,'Game_count_in_cart':Game_count_in_cart})


def remove_from_cart_view(request,pk):
    #for counter in cart
    if 'Game_ids' in request.COOKIES:
        Game_ids = request.COOKIES['Game_ids']
        counter=Game_ids.split('|')
        Game_count_in_cart=len(set(counter))
    else:
        Game_count_in_cart=0

    # removing game id from cookie
    total=0
    if 'Game_ids' in request.COOKIES:
        Game_ids = request.COOKIES['Game_ids']
        Game_id_in_cart=Game_ids.split('|')
        Game_id_in_cart=list(set(Game_id_in_cart))
        Game_id_in_cart.remove(str(pk))
        Games=models.Game.objects.all().filter(id__in = Game_id_in_cart)
        #for total price shown in cart after removing game
        for p in Games:
            total=total+p.price

        #  for update coookie value after removing game id in cart
        value=""
        for i in range(len(Game_id_in_cart)):
            if i==0:
                value=value+Game_id_in_cart[0]
            else:
                value=value+"|"+Game_id_in_cart[i]
        response = render(request, 'gamepages/cart.html',{'Games':Games,'total':total,'Game_count_in_cart':Game_count_in_cart})
        if value=="":
            response.delete_cookie('Game_ids')
        response.set_cookie('Game_ids',value)
        return response
    


def send_feedback_view(request):
    feedbackForm=forms.FeedbackForm()
    if request.method == 'POST':
        feedbackForm = forms.FeedbackForm(request.POST)
        if feedbackForm.is_valid():
            feedbackForm.save()
            return render(request, 'ecom/feedback_sent.html')
    return render(request, 'gamepages/send_feedback.html', {'feedbackForm':feedbackForm})


def send_cont_view(request):
    contForm=forms.ContForm()
    if request.method == 'POST':
        contForm = forms.ContForm(request.POST)
        if contForm.is_valid():
            contForm.save()
            return render(request, 'gamepages/home.html')
    return render(request, 'gamepages/contact.html', {'contForm':contForm})


#---------------------------------------------------------------------------------
#------------------------ CUSTOMER RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_home_view(request):
    Games=models.Game.objects.all()
    Advertises=models.Advertises.objects.all()
    News=models.News.objects.all()
    if 'Game_ids' in request.COOKIES:
        Game_ids = request.COOKIES['Game_ids']
        counter=Game_ids.split('|')
        Game_count_in_cart=len(set(counter))
    else:
        Game_count_in_cart=0
    
    return render(request,'gamepages/home.html',{'Games':Games,'News':News,'Advertises':Advertises,'Game_count_in_cart':Game_count_in_cart})



# shipment address before placing order
@login_required(login_url='customerlogin')
def customer_address_view(request):
    # this is for checking whether game is present in cart or not
    # if there is no game in cart we will not show address form
    Game_in_cart=False
    if 'Game_ids' in request.COOKIES:
        Game_ids = request.COOKIES['Game_ids']
        if Game_ids != "":
            Game_in_cart=True
    #for counter in cart
    if 'Game_ids' in request.COOKIES:
        Game_ids = request.COOKIES['Game_ids']
        counter=Game_ids.split('|')
        Game_count_in_cart=len(set(counter))
    else:
        Game_count_in_cart=0

    addressForm = forms.AddressForm()
    if request.method == 'POST':
        addressForm = forms.AddressForm(request.POST)
        if addressForm.is_valid():
            # here we are taking address, email, mobile at time of order placement
            # we are not taking it from customer account table because
            # these thing can be changes
            email = addressForm.cleaned_data['Email']
            mobile=addressForm.cleaned_data['Mobile']
            address = addressForm.cleaned_data['Address']
            #for showing total price on payment page.....accessing id from cookies then fetching  price of game from db
            total=0
            if 'Game_ids' in request.COOKIES:
                Game_ids = request.COOKIES['Game_ids']
                if Game_ids != "":
                    Game_id_in_cart=Game_ids.split('|')
                    Games=models.Game.objects.all().filter(id__in = Game_id_in_cart)
                    for p in Games:
                        total=total+p.price

            response = render(request, 'gamepages/payment.html',{'total':total})
            response.set_cookie('email',email)
            response.set_cookie('mobile',mobile)
            response.set_cookie('address',address)
            return response
    return render(request,'gamepages/customer_address.html',{'addressForm':addressForm,'Game_in_cart':Game_in_cart,'Game_count_in_cart':Game_count_in_cart})




# here we are just directing to this view...actually we have to check whther payment is successful or not
#then only this view should be accessed
@login_required(login_url='customerlogin')
def payment_success_view(request):
    # Here we will place order | after successful payment
    # we will fetch customer  mobile, address, Email
    # we will fetch game id from cookies then respective details from db
    # then we will create order objects and store in db
    # after that we will delete cookies because after order placed...cart should be empty
    customer=models.Customer.objects.get(user_id=request.user.id)
    Games=None
    email=None
    mobile=None
    address=None
    if 'Game_ids' in request.COOKIES:
        Game_ids = request.COOKIES['Game_ids']
        if Game_ids != "":
            Game_id_in_cart=Game_ids.split('|')
            Games=models.Game.objects.all().filter(id__in = Game_id_in_cart)
            # Here we get Games list that will be ordered by one customer at a time

    # these things can be change so accessing at the time of order...
    if 'email' in request.COOKIES:
        email=request.COOKIES['email']
    if 'mobile' in request.COOKIES:
        mobile=request.COOKIES['mobile']
    if 'address' in request.COOKIES:
        address=request.COOKIES['address']

    # here we are placing number of orders as much there is a Games
    # suppose if we have 5 items in cart and we place order....so 5 rows will be created in orders table
    # there will be lot of redundant data in orders table...but its become more complicated if we normalize it
    for game in Games:
        models.Orders.objects.get_or_create(customer=customer,game=game,status='Pending',email=email,mobile=mobile,address=address)

    # after order placed cookies should be deleted
    response = render(request,'ecom/payment_success.html')
    response.delete_cookie('Game_ids')
    response.delete_cookie('email')
    response.delete_cookie('mobile')
    response.delete_cookie('address')
    return response




@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def my_order_view(request):
    
    customer=models.Customer.objects.get(user_id=request.user.id)
    orders=models.Orders.objects.all().filter(customer_id = customer)
    ordered_Games=[]
    for order in orders:
        ordered_Game=models.Game.objects.all().filter(id=order.game.id)
        ordered_Games.append(ordered_Game)

    return render(request,'ecom/my_order.html',{'data':zip(ordered_Games,orders)})
 



# @login_required(login_url='customerlogin')
# @user_passes_test(is_customer)
# def my_order_view2(request):

#     Games=models.Game.objects.all()
#     if 'Game_ids' in request.COOKIES:
#         Game_ids = request.COOKIES['Game_ids']
#         counter=Game_ids.split('|')
#         Game_count_in_cart=len(set(counter))
#     else:
#         Game_count_in_cart=0
#     return render(request,'ecom/my_order.html',{'Games':Games,'Game_count_in_cart':Game_count_in_cart})    



#--------------for discharge patient bill (pdf) download and printing
import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return

@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def download_invoice_view(request,orderID,GameID):
    order=models.Orders.objects.get(id=orderID)
    game=models.Game.objects.get(id=GameID)
    mydict={
        'orderDate':order.order_date,
        'customerName':request.user,
        'customerEmail':order.email,
        'customerMobile':order.mobile,
        'shipmentAddress':order.address,
        'orderStatus':order.status,

        'GameName':game.name,
        'GameImage':game.game_image,
        'GamePrice':game.price,
        'GameDescription':game.description,


    }
    return render_to_pdf('ecom/download_invoice.html',mydict)






@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def my_profile_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    return render(request,'ecom/my_profile.html',{'customer':customer})


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def edit_profile_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    user=models.User.objects.get(id=customer.user_id)
    userForm=forms.CustomerUserForm(instance=user)
    customerForm=forms.CustomerForm(request.FILES,instance=customer)
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST,instance=user)
        customerForm=forms.CustomerForm(request.POST,instance=customer)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customerForm.save()
            return HttpResponseRedirect('my-profile')
    return render(request,'ecom/edit_profile.html',context=mydict)



#---------------------------------------------------------------------------------
#------------------------ ABOUT US AND CONTACT US VIEWS START --------------------
#---------------------------------------------------------------------------------
def aboutus_view(request):
    return render(request,'gamepages/contact.html')

def home_view(request):
    Games=models.Game.objects.all()
    Advertises=models.Advertises.objects.all()
    News=models.News.objects.all()
    if 'Game_ids' in request.COOKIES:
        Game_ids = request.COOKIES['Game_ids']
        counter=Game_ids.split('|')
        Game_count_in_cart=len(set(counter))
    else:
        Game_count_in_cart=0
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'gamepages/home.html',{'Games':Games,'News':News,'Advertises':Advertises,'Game_count_in_cart':Game_count_in_cart})





def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message, settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'gamepages/home.html')
    return render(request, 'gamepages/contact.html', {'form':sub})




def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = models.User.objects.get(email=email)
                customer = Customer.objects.get(user=user)
                customer.send_password_reset_email()
                messages.success(request, 'An email with instructions to reset your password has been sent.')
                return redirect('customerlogin')  # Redirect to the login page or any other desired page
            except models.User.DoesNotExist:
                pass
    else:
        form = PasswordResetForm()
    return render(request, 'ecom/password_reset_request.html', {'form': form})


def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = models.User.objects.get(pk=uid)
        customer = Customer.objects.get(user=user)
        if default_token_generator.check_token(user, token):
            if request.method == 'POST':
                form = SetPasswordForm(user, request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Your password has been reset successfully.')
                    return redirect('customerlogin')  # Redirect to the login page or any other desired page
            else:
                form = SetPasswordForm(user)
            return render(request, 'ecom/password_reset_confirm.html', {'form': form})
    except (TypeError, ValueError, OverflowError, models.User.DoesNotExist):
        pass
    messages.error(request, 'The password reset link is invalid or has expired.')
    return redirect('customerlogin')  # Redirect to the login page or any other desired page
