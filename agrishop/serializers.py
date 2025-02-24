from rest_framework import serializers
from .models import CustomUser, Product, Cart, LandBidding, Bid
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'full_name', 'phone_number', 'address', 'role', 'business_name', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'full_name': {'required': True}
        }

    def validate(self, data):
        if data.get('role') == 'seller' and not data.get('business_name'):
            raise serializers.ValidationError({"business_name": "Sellers must provide a business name."})
        return data

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])  # Hash password
        return CustomUser.objects.create(**validated_data)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class CartSerializer(serializers.ModelSerializer):
    product_details = ProductSerializer(source='product', read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'product', 'product_details', 'quantity', 'added_at', 'total_price']
        read_only_fields = ['added_at']

    def get_total_price(self, obj):
        return obj.total_price()

    def validate(self, data):
        # Ensure quantity doesn't exceed product availability
        product = data.get('product')
        quantity = data.get('quantity', 1)
        
        if product and quantity > product.quantity:
            raise serializers.ValidationError({
                'quantity': f'Cannot add more than available stock ({product.quantity})'
            })
        return data

class LandBiddingSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(
        read_only=True, 
        default=serializers.CurrentUserDefault()
    )
    total_bids = serializers.SerializerMethodField()

    class Meta:
        model = LandBidding
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'status']

    def get_total_bids(self, obj):
        return obj.bids.count()

class BidSerializer(serializers.ModelSerializer):
    bidder = serializers.PrimaryKeyRelatedField(
        read_only=True, 
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Bid
        fields = '__all__'
        read_only_fields = ['bid_time']

    def validate(self, data):
        # Validate bid amount is higher than current highest bid
        land_listing = data.get('land_listing')
        bid_amount = data.get('bid_amount')

        if land_listing:
            # Get the current highest bid
            highest_bid = land_listing.bids.order_by('-bid_amount').first()
            
            if highest_bid and bid_amount <= highest_bid.bid_amount:
                raise serializers.ValidationError({
                    'bid_amount': f'Bid must be higher than the current highest bid of {highest_bid.bid_amount}'
                })

            # Ensure bid is above starting bid amount
            if bid_amount < land_listing.starting_bid_amount:
                raise serializers.ValidationError({
                    'bid_amount': f'Bid must be at least the starting bid amount of {land_listing.starting_bid_amount}'
                })

        return data