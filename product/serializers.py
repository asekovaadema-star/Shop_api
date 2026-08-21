from rest_framework import serializers
from .models import Category, Product, Review


class ProductDetailListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product  
        fields = "__all__"


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product 
        fields = ("id", "price")  


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category  
        fields = "__all__"  


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