
from django.http import Http404
from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import ProductSerializer
from .models import Product
 
class ProductList(APIView):
    def post(self, request):
        note = ProductSerializer(data=request.data, context={'request': request})  # Pass request context
        if note.is_valid(raise_exception=True):
            note.save()
            return Response(note.data, status=status.HTTP_201_CREATED)
 
        return Response(note.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        # 1. Mengambil parameter query 'name' dan 'location' dari URL (Advanced 4 pts)
        name_query = request.query_params.get('name', None)
        location_query = request.query_params.get('location', None)
        
        # 2. Filter awal: Hanya produk yang belum di-soft delete
        products = Product.objects.filter(is_delete=False)
        
        # 3. Menerapkan pencarian berdasarkan nama jika parameter 'name' tersedia
        if name_query is not None:
            products = products.filter(name__icontains=name_query)
            
        # 4. Menerapkan pencarian berdasarkan lokasi jika parameter 'location' tersedia (Advanced 4 pts)
        if location_query is not None:
            products = products.filter(location__icontains=location_query)
            
        # 5. Menggunakan serializer untuk menampilkan data produk (Advanced 4 pts)
        serializer = ProductSerializer(products, many=True, context={'request': request})
        
        # 6. Mengembalikan response dengan key "products" (Skilled 3 pts)
        # Jika data tidak ditemukan, serializer.data akan otomatis menjadi list kosong []
        return Response({
            "products": serializer.data
        }, status=status.HTTP_200_OK)      

class ProductDetail(APIView):
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(product, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        product = self.get_object(pk)
        
        # Menerapkan logic Soft Delete
        product.is_delete = True
        product.save()
        
        return Response(status=status.HTTP_204_NO_CONTENT)