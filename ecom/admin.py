from django.contrib import admin
from .models import Customer,Game,Orders,Feedback,News,Advertises,CrackGame,Contact,UserAdvertises
# Register your models here.
class CustomerAdmin(admin.ModelAdmin):
    pass
admin.site.register(Customer, CustomerAdmin)

class GameAdmin(admin.ModelAdmin):
    pass
admin.site.register(Game, GameAdmin)

class CrackGameAdmin(admin.ModelAdmin):
    pass
admin.site.register(CrackGame, CrackGameAdmin)

class NewsAdmin(admin.ModelAdmin):
    pass
admin.site.register(News, NewsAdmin)

class AdvertisesAdmin(admin.ModelAdmin):
    pass
admin.site.register(Advertises, AdvertisesAdmin)



class UserAdvertisesAdmin(admin.ModelAdmin):
    pass
admin.site.register(UserAdvertises, UserAdvertisesAdmin)

class OrderAdmin(admin.ModelAdmin):
    pass
admin.site.register(Orders, OrderAdmin)

class FeedbackAdmin(admin.ModelAdmin):
    pass
admin.site.register(Feedback, FeedbackAdmin)

class ContactAdmin(admin.ModelAdmin):
    pass
admin.site.register(Contact, ContactAdmin)
# Register your models here.
