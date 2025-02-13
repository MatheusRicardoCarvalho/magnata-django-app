from django.contrib import admin
from .models import StockInWallet,Stock,Sector,BuyHistory,Classification,User,UserFollowWallet,Wallet, SellHistory
# Register your models here.

admin.site.register(Wallet)
admin.site.register(UserFollowWallet)
admin.site.register(Sector)
admin.site.register(BuyHistory)
admin.site.register(Stock)
admin.site.register(StockInWallet)
admin.site.register(Classification)
admin.site.register(SellHistory)





