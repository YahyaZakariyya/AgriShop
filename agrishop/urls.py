from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, ProductViewSet, 
    CartViewSet, LandBiddingViewSet, BidViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'products', ProductViewSet)
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'land-listings', LandBiddingViewSet)
router.register(r'bids', BidViewSet, basename='bid')

urlpatterns = [
    path('', include(router.urls)),
]