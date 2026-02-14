# from django.urls import path
# from app.product.views import ProductListAPIView, ProductDetailAPIView, ProductCreateAPIView

# urlpatterns = [
#     path("products/", ProductListAPIView.as_view(), name='product-list'),
#     path("products/<uuid:uuid>/", ProductDetailAPIView.as_view(), name='prodcut-detail'),
#     path("product/create/", ProductCreateAPIView.as_view(), name='create')
# ]


from rest_framework.routers import DefaultRouter
from app.product.views import ProductViewSet

router = DefaultRouter()
router.register("products", ProductViewSet, basename="products")

urlpatterns = router.urls