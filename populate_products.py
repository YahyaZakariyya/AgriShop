import random
import os
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce.settings")
django.setup()

from agrishop.models import Product, Category  # Replace 'your_app' with your 

# Sample fertilizer product data (Expanded to 20 unique items)
fertilizers = [
    {"title": "Urea", "description": "High nitrogen content for plant growth.", "price": 25.50},
    {"title": "DAP (Diammonium Phosphate)", "description": "Rich in phosphorus, essential for root development.", "price": 30.75},
    {"title": "NPK 15-15-15", "description": "Balanced nutrients for overall plant health.", "price": 40.00},
    {"title": "Potassium Nitrate", "description": "Boosts fruit development and stress tolerance.", "price": 45.00},
    {"title": "Super Phosphate", "description": "Provides phosphorus for root and flower growth.", "price": 28.99},
    {"title": "Calcium Nitrate", "description": "Essential for cell wall strength and disease resistance.", "price": 35.50},
    {"title": "Zinc Sulphate", "description": "Improves enzymatic activities in plants.", "price": 18.99},
    {"title": "Magnesium Sulphate", "description": "Prevents yellowing of leaves and enhances photosynthesis.", "price": 22.50},
    {"title": "Ammonium Sulphate", "description": "Good nitrogen source for alkaline soils.", "price": 20.75},
    {"title": "Rock Phosphate", "description": "Organic phosphate fertilizer for long-term phosphorus release.", "price": 32.00},
    {"title": "Muriate of Potash", "description": "Excellent source of potassium for plant growth.", "price": 37.99},
    {"title": "Sulfur-Coated Urea", "description": "Controlled-release nitrogen fertilizer.", "price": 50.00},
    {"title": "Epsom Salt", "description": "Provides magnesium and sulfur for better chlorophyll production.", "price": 15.99},
    {"title": "Bone Meal", "description": "Rich in phosphorus for strong root development.", "price": 29.99},
    {"title": "Blood Meal", "description": "Organic nitrogen fertilizer to boost plant growth.", "price": 33.50},
    {"title": "Fish Emulsion", "description": "Organic liquid fertilizer for rapid plant uptake.", "price": 27.99},
    {"title": "Seaweed Extract", "description": "Enhances plant immunity and stress tolerance.", "price": 45.99},
    {"title": "Vermicompost", "description": "Nutrient-rich compost made from earthworms.", "price": 18.50},
    {"title": "Compost Tea", "description": "Liquid organic fertilizer rich in beneficial microbes.", "price": 19.99},
    {"title": "Neem Cake", "description": "Organic fertilizer and pest repellent.", "price": 24.75},
]

# Ensure at least one category exists
default_category, _ = Category.objects.get_or_create(name="Fertilizers")

# Populate the database with 50 records
for _ in range(50):
    data = random.choice(fertilizers)
    product = Product.objects.create(
        title=data["title"],
        description=data["description"],
        category=default_category,
        quantity=random.randint(10, 500),  # Random stock quantity
        price=round(data["price"] * (0.9 + random.uniform(0, 0.2)), 2),  # Small variation in price
    )
    print(f"Added: {product.title}")

print("✅ Database successfully populated with 50 products.")
