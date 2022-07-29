from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Collection, Product
from .serializers import COllectionSerializer, ProductSerializer
from store import serializers


class ProductList(APIView):
    def get(self, request):
        queryset = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(
            queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductDetail(APIView):

    def get(self, request,id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request,id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product=product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request,id):
        product = get_object_or_404(Product, pk=id)
        if product.orderitems.count() > 0:
            return Response({'error': "Product cannot be deleted because it has been ordered"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def collection_list(request):
    if request.method == 'GET':
        queryset = Collection.objects.annotate(
            products_count=Count('product')
        ).all()
        serializer = COllectionSerializer(queryset, many=True, context={
            'request': request
        })
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = COllectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def collection_detail(request, id):

    collection = get_object_or_404(
        Collection.objects.annotate(
            products_count=Count('products'), pk=id)
    )
    if request.method == 'GET':

        serializer = COllectionSerializer(collection,)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = COllectionSerializer(
            collection,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

    elif request.metho == 'DELETE':
        if collection.products.count() > 0:
            return Response({'error': 'Collection cannot be deleted as it already in use'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
