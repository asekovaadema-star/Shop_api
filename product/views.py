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
                          ReviewListSerializer)

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
        product.title = request.data.get('title')
        product.description = request.data.get('description')
        product.price = request.data.get('price')
        product.category_id = request.data.get('category_id')
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
        title = requset.data.get('title')
        description = requset.data.get('description')
        price = requset.data.get('price')
        category_id = requset.data.get('category_id')

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
        name = request.data.get('name')

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
        category.name = request.data.get('name')
        category.save()
        return Response(status=status.HTTP_201_CREATED, 
                        data=CategoryDetailSerializer(category).data)


@api_view(['GET', 'POST'])

def review_create_list_api_view(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        list_ = ReviewListSerializer(reviews, many = True).data
        return Response(
            status=status.HTTP_200_OK, 
            data = list_
        )
    elif request.method == 'POST':
        text = request.data.get('text')
        stars = request.data.get('stars')
        product_id = request.data.get('product_id')

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
        review.text = request.data.get('text')
        review.stars = request.data.get('stars')
        review.product_id = request.data.get('product_id')
        review.save()
        return Response(status=status.HTTP_201_CREATED, 
                        data=ReviewDetailSerializer(review).data)

