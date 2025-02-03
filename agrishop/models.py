from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MinValueValidator
from PIL import Image
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
import uuid

class CustomUserManager(BaseUserManager):
    def create_user(self, email, full_name, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        
        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.email

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Categories'

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='products'
    )
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(0)]
    )
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        upload_to='product_images/', 
        blank=True, 
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        if self.image:
            img = Image.open(self.image.path)
            img.thumbnail((800, 600))
            img.save(self.image.path)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='cart')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        default=1
    )
    added_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return self.product.price * self.quantity

    class Meta:
        unique_together = ('user', 'product')
        verbose_name_plural = 'Cart Items'

class LandBidding(models.Model):
    CITY_CHOICES = [
        ('lahore', 'Lahore'),
        ('karachi', 'Karachi'),
        ('islamabad', 'Islamabad'),
        ('rawalpindi', 'Rawalpindi'),
        ('other', 'Other')
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('pending', 'Pending'),
        ('closed', 'Closed')
    ]

    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='land_listings')
    title = models.CharField(max_length=255)
    description = models.TextField()
    city = models.CharField(max_length=20, choices=CITY_CHOICES, default='other')
    area_size = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0)]
    )
    starting_bid_amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        validators=[MinValueValidator(0)]
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.city}"

class Bid(models.Model):
    land_listing = models.ForeignKey(LandBidding, on_delete=models.CASCADE, related_name='bids')
    bidder = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    bid_amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        validators=[MinValueValidator(0)]
    )
    bid_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bid by {self.bidder.full_name} - {self.bid_amount}"

    class Meta:
        ordering = ['-bid_amount']