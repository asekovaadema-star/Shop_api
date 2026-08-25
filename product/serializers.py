from rest_framework import serializers
from .models import Category, Product, Review

class CategoryListSerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()
    class Meta:
        model = Category  
        fields = ('id', 'name', 'product_count')

    def get_product_count(self, obj):
        return len([product for product in obj.products.all()])



class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category  
        fields = "__all__"  


class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review  
        fields = (
            "product",
        ) 

class ReviewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review  
        fields = "__all__" 

class ProductDetailListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product  
        fields = "__all__"


class ProductListSerializer(serializers.ModelSerializer):
    reviews = ReviewDetailSerializer(many = True)
    rating = serializers.SerializerMethodField()
    class Meta:
        model = Product 
        fields = ("title",
                  "id", 
                  "price", 
                  "reviews",
                  'rating') 

    def get_rating(self, obj):
        stars = [review.stars for review in obj.reviews.all()]
        return round(sum(stars)/ len(stars), 1 ) if stars else 0.0