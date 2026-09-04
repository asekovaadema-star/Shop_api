from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status 
from product.models import Product, Category, Review
from django.forms import model_to_dict
from .serializers import ( ProductListSerializer, 
                          ProductDetailListSerializer, 
                          CategoryDetailSerializer, 
                          CategoryListSerializer, 
                          ReviewDetailSerializer, 
                          ReviewListSerializer, 
                          ProductValidateSerializer, 
                          CategoryValidateSerializer,
                          ReviewValidateSerializer, 
                          )
from django.db import transaction

@api_view(['GET', 'PUT', 'DELETE'])

def product_datail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(data={'error': 'Product not found'}, 
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = ProductDetailListSerializer(product, many = False).data
        return Response(data=data)
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        serializer = ProductValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                             data=serializer.errors)
        print(request.data)
        print(serializer.validated_data)

        with transaction.atomic():
            product.title = serializer.validated_data.get('title')
            product.description = serializer.validated_data.get('description')
            product.price = serializer.validated_data.get('price')
            product.category_id = serializer.validated_data.get('category_id')
            product.save()
        return Response(status=status.HTTP_201_CREATED, 
                        data= ProductDetailListSerializer(product).data)


@api_view(['GET', 'POST'])

def product_create_list_api_view(requset):
    if requset.method == 'GET':
        products = Product.objects.all()
        list_ = ProductListSerializer(products, many = True).data
        return Response(
            status=status.HTTP_200_OK, 
            data=list_)
    elif requset.method == 'POST':

        #step 0: Validation (Existing, Typing, Extra)
        serializer = ProductValidateSerializer(data=requset.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, 
                            data=serializer.errors)
        print(requset.data)
        print(serializer.validated_data)
        
        title = serializer.validated_data.get('title')
        description = serializer.validated_data.get('description')
        price = serializer.validated_data.get('price')
        category_id = serializer.validated_data.get('category_id')

        with transaction.atomic():
            product = Product.objects.create(
                title=title, 
                description = description, 
                price = price, 
                category_id=category_id,
            )
            product.save()

        return Response(data=ProductDetailListSerializer(product).data, 
                        status=status.HTTP_201_CREATED)

@api_view(['GET', 'POST'])

def category_create_list_api_view(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        list_ = CategoryListSerializer(categories, many = True).data
        return Response(
            status=status.HTTP_200_OK, 
            data = list_
        )
    elif request.method == 'POST':
        serializer = CategoryValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, 
                            data=serializer.errors)
        print(request.data)
        print(serializer.validated_data)

        name = serializer.validated_data.get('name')

        with transaction.atomic():
            category = Category.objects.create(
                name = name 
            )
            category.save()
        return Response(data=CategoryDetailSerializer(category).data, 
                        status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])

def categiry_detail_api_view(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(data={'error': 'Categoty not found'}, 
                        status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        data  = CategoryDetailSerializer(category, many = False).data
        return Response(data=data)
    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.mehtod == 'PUT':
        serializer = CategoryValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, 
                            data=serializer.errors)
        print(request.data)
        print(serializer.validated_data)

        with transaction.atomic():
            category.name = serializer.validated_data.get('name')
            category.save()
        return Response(status=status.HTTP_201_CREATED, 
                        data=CategoryDetailSerializer(category).data)


@api_view(['GET', 'POST'])

def review_create_list_api_view(request):
    print(request.user)
    if request.method == 'GET':
        reviews = Review.objects.all()
        list_ = ReviewListSerializer(reviews, many = True).data
        return Response(
            status=status.HTTP_200_OK, 
            data = list_
        )
    elif request.method == 'POST':
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, 
                            data=serializer.errors)
        print(request.data)
        print(serializer.validated_data)

        text = serializer.validated_data.get('text')
        stars = serializer.validated_data.get('stars')
        product_id = serializer.validated_data.get('product_id')

        with transaction.atomic():
            review = Review.objects.create(
                text = text, 
                stars = stars, 
                product_id= product_id, 
            )
            review.save()
        return Response(data=ReviewDetailSerializer(review).data, 
                        status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])

def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'error': 'Review not found'}, 
                        status=status.HTTP_404_NOT_FOUND)

    if request.mehtod =='GET':
        data  = ReviewDetailSerializer(review, many = False).data
        return Response(data=data)
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, 
                            data=serializer.errors)

        with transaction.atomic():
            review.text = serializer.validated_data.get('text')
            review.stars = serializer.validated_data.get('stars')
            review.product_id = serializer.validated_data.get('product_id')
            review.save()
        return Response(status=status.HTTP_201_CREATED, 
                        data=ReviewDetailSerializer(review).data)

