from rest_framework import serializers
from .models import Category, Product, Review
from rest_framework.exceptions import ValidationError

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

class ProductValidateSerializer(serializers.Serializer):
    title = serializers.CharField(required = True, max_length=50, min_length=1)
    description = serializers.CharField(required = False)
    price = serializers.FloatField()
    category_id = serializers.IntegerField(default = 1)

    def validate_category_id(self, category_id):
        try:
            Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise ValidationError('Category not found!')
        return category_id

class CategoryValidateSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)

class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField(required = True, max_length= 255, min_length=1)
    stars = serializers.IntegerField(max_value=10, min_value= 1)
    product_id=serializers.IntegerField()

    def validate_product_id(self, product_id):
        try:
            Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise ValidationError('Product not found!')
        return product_id


    


