# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from django.core.cache import cache
# from django.shortcuts import get_object_or_404
# from rest_framework.generics import CreateAPIView

# from app.product.models import Product
# from app.product.serializers import ProductSerializer, ProductDetailSerializer, ProductCreateSerializer

# class ProductCreateAPIView(CreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductCreateSerializer

# class ProductListAPIView(APIView):
#     def get(self, request):
#         cache_key = "product_list"
#         cached_data = cache.get(cache_key)

#         if cached_data:
#             # print("\n\n\n\nCache\n\n\n\n")
#             return Response(cached_data, status=status.HTTP_200_OK)

#         # print("\n\n\n\nDB\n\n\n\n")

#         products = (
#             Product.objects
#             .select_related("category", "model")
#             .prefetch_related("images")
#             .order_by("-created_at")
#         )
#         serializer = ProductSerializer(products, many=True)
#         cache.set(cache_key, serializer.data, timeout=60 * 2)
#         return Response(serializer.data, status=status.HTTP_200_OK)

# class ProductDetailAPIView(APIView):
    
#     def get_object(self, uuid):
#         return get_object_or_404(
#             Product.objects.select_related("category", "model")
#             .prefetch_related("images"), uuid=uuid
#         )

#     def get(self, request, uuid):
#         serializer = ProductDetailSerializer(self.get_object(uuid))
#         return Response(serializer.data)
    
#     def put(self, request, uuid):
#         product = self.get_object(uuid)
#         serializer = ProductDetailSerializer(product, data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             cache.delete("product_list")
#             return Response(serializer.data)

#         return Response(serializer.errors, status=400)
        
#     def patch(self, request, uuid):
#         product = self.get_object(uuid)
#         serializer = ProductDetailSerializer(product, data=request.data, partial=True)

#         if serializer.is_valid():
#             serializer.save()
#             cache.delete("product_list")
#             return Response(serializer.data)

#         return Response(serializer.errors, status=400)

#     def delete(self, request, uuid):
#         self.get_object(uuid).delete()
#         cache.delete("product_list")
#         return Response(status=204)


from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, AllowAny

from app.product.models import Product
from app.product.serializers import (
    ProductSerializer,
    ProductCreateSerializer,
    ProductDetailSerializer,
)
from app.pagination import CustomPageNumberPagination
from app.filters import ProductFilter


class ProductViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin, 
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    GenericViewSet):
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    def get_queryset(self):
        return Product.objects.select_related("category", "model").prefetch_related("images").order_by("-created_at")
    
    def get_serializer_class(self):
        if self.action == "create":
            return ProductCreateSerializer
        elif self.action == "retrieve":
            return ProductDetailSerializer
        return ProductSerializer

    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated()]
        return [AllowAny()]