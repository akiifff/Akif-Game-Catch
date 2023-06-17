
from django.contrib import admin
from django.urls import path
from ecom import views



from django.contrib.auth.views import LoginView,LogoutView,PasswordResetDoneView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home_view,name=''),
    path('detailgameview/<int:pk>',views.detail_game_view,name='detailgameview'),
    path('detailcrackgameview/<int:pk>',views.detail_crack_game_view,name='detailcrackgameview'),
    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('logout', LogoutView.as_view(template_name='gamepages/home.html'),name='logout'),
    path('aboutus', views.aboutus_view),
    path('contactus', views.contactus_view,name='contactus'),
    path('search', views.search_view,name='search'),
    path('send-feedback', views.send_feedback_view,name='send-feedback'),
    path('send-cont', views.send_cont_view,name='send-cont'),
    path('allgames', views.allgames,name='allgames'),
    path('allcrackgames', views.allcrackgames,name='allcrackgames'),
    path('view-feedback', views.view_feedback_view,name='view-feedback'),
    path('view-ads', views.user_UserAdvertises_view,name='view-ads'),

    path('adminclick', views.adminclick_view),
    path('adminlogin', LoginView.as_view(template_name='ecom/adminlogin.html'),name='adminlogin'),
    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),

    path('view-customer', views.view_customer_view,name='view-customer'),
    path('delete-customer/<int:pk>', views.delete_customer_view,name='delete-customer'),
    path('update-customer/<int:pk>', views.update_customer_view,name='update-customer'),

    path('admin-Games', views.admin_Games_view,name='admin-Games'),
    path('admin-add-game', views.admin_add_Game_view,name='admin-add-game'),
    path('delete-game/<int:pk>', views.delete_Game_view,name='delete-game'),
    path('update-game/<int:pk>', views.update_Game_view,name='update-game'),
    
    
    path('admin-CrackGames', views.admin_CrackGames_view,name='admin-CrackGames'),
    path('admin-add-crackgame', views.admin_add_CrackGame_view,name='admin-add-crackgame'),
    path('delete-crackgame/<int:pk>', views.delete_CrackGame_view,name='delete-crackgame'),
    path('update-crackgame/<int:pk>', views.update_CrackGame_view,name='update-crackgame'),
    
    
    path('admin-News', views.admin_News_view,name='admin-News'),
    path('admin-add-news', views.admin_add_News_view,name='admin-add-news'),
    path('delete-news/<int:pk>', views.delete_News_view,name='delete-news'),
    path('update-news/<int:pk>', views.update_News_view,name='update-news'),
    # path('admin-approve-Driving', views.admin_approve_Driving_view,name='admin-approve-Driving'),
    path('approve-Add/<int:pk>', views.approve_Add_view,name='approve-Add'),

    path('reject-Add/<int:pk>', views.reject_Add_view,name='reject-Add'),

    path('admin-Advertises', views.admin_Advertises_view,name='admin-Advertises'),
    path('admin-UserAdvertises', views.admin_UserAdvertises_view,name='admin-UserAdvertises'),
    path('user-Advertises', views.user_Advertises_view,name='user-Advertises'),
    path('admin-add-advertises', views.admin_add_Advertises_view,name='admin-add-advertises'),
    path('customer-add-advertises', views.customer_add_Advertises_view,name='customer-add-advertises'),
    path('delete-advertises/<int:pk>', views.delete_Advertises_view,name='delete-advertises'),
    path('update-advertises/<int:pk>', views.update_Advertises_view,name='update-advertises'),


    path('admin-view-booking', views.admin_view_booking_view,name='admin-view-booking'),
    path('delete-order/<int:pk>', views.delete_order_view,name='delete-order'),
    path('update-order/<int:pk>', views.update_order_view,name='update-order'),


    path('customersignup', views.customer_signup_view),
    path('customernews', views.customer_News_view),
    path('customerlogin', LoginView.as_view(template_name='ecom/customerlogin.html'),name='customerlogin'),
    path('customer-home', views.customer_home_view,name='customer-home'),
    path('my-order', views.my_order_view,name='my-order'),
    # path('my-order', views.my_order_view2,name='my-order'),
    path('my-profile', views.my_profile_view,name='my-profile'),
    path('edit-profile', views.edit_profile_view,name='edit-profile'),
    path('download-invoice/<int:orderID>/<int:GameID>', views.download_invoice_view,name='download-invoice'),


    path('add-to-cart/<int:pk>', views.add_to_cart_view,name='add-to-cart'),
    path('cart', views.cart_view,name='cart'),
    path('remove-from-cart/<int:pk>', views.remove_from_cart_view,name='remove-from-cart'),
    path('customer-address', views.customer_address_view,name='customer-address'),
    path('payment-success', views.payment_success_view,name='payment-success'),

    
    path('password-reset/', views.password_reset_request, name='password_reset_request'),
    path('reset-password/<str:uidb64>/<str:token>/', views.password_reset_confirm, name='password_reset_confirm'),

    



]
