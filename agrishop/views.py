from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import CustomUser, Product, Cart, LandBidding, Bid
from .serializers import (
    UserSerializer, ProductSerializer, 
    CartSerializer, LandBiddingSerializer, BidSerializer
)

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at']

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class LandBiddingViewSet(viewsets.ModelViewSet):
    queryset = LandBidding.objects.all()
    serializer_class = LandBiddingSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['city', 'status']
    search_fields = ['title', 'description']

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    @action(detail=True, methods=['POST'])
    def place_bid(self, request, pk=None):
        land_listing = self.get_object()
        serializer = BidSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(
                land_listing=land_listing, 
                bidder=request.user
            )
            return Response(serializer.data, status=201)
        
        return Response(serializer.errors, status=400)

class BidViewSet(viewsets.ModelViewSet):
    serializer_class = BidSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Bid.objects.filter(bidder=self.request.user)