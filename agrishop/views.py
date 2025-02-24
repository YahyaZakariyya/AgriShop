from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django_filters.rest_framework import DjangoFilterBackend
from .models import CustomUser, Product, Cart, LandBidding, Bid, Category
from .serializers import UserSerializer, ProductSerializer, CartSerializer, LandBiddingSerializer, BidSerializer, CategorySerializer 

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

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        product = serializer.validated_data.get('product')
        quantity = serializer.validated_data.get('quantity', 1)

        # Check if enough stock is available
        if product.quantity < quantity:
            raise ValidationError({"quantity": f"Only {product.quantity} items are available in stock."})

        # Assign logged-in user
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
    
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Generate JWT token for auto-login after registration
            refresh = RefreshToken.for_user(user)

            return Response({
                "user": UserSerializer(user).data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, username=email, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            })
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)