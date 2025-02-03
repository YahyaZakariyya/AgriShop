from django.contrib import admin
from .models import CustomUser, Category, Product, Cart, LandBidding, Bid

admin.site.register(CustomUser)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(LandBidding)
admin.site.register(Bid)