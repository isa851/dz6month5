from rest_framework import serializers

from app.product.models import Category, Models, Product, ProductImage

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']

class ProductSerializer(serializers.ModelSerializer):
    first_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            'user',
            "uuid",
            "title",
            "description",
            "price",
            "first_image"
        ]

    def get_first_image(self, obj):
        first_img = obj.images.first()
        if first_img:
            return first_img.image.url
        return None

class ProductDetailSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    category_title = serializers.CharField(source='category.title', read_only=True)
    model_title = serializers.CharField(source='model.title', read_only=True)

    class Meta:
        model = Product
        fields = [
            "id","user", "uuid", "title", 
            "description", "price", 
            "created_at", "size", 
            "is_active", "is_favorite", 
            "images", "model_title", "category_title"
        ]

class ProductCreateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Product
        fields = [
            'title','description', 'price', 'size',
            'category', 'model', 'images'
        ]

    def validate_title(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Название должно быть минимум 3 символа!")
        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Цена должно быть больше 0!")
        return value

    def validate_size(self, value):
        if len(value) > 10:
            raise serializers.ValidationError("Размер слишком длинный!")
        return value

    def validate(self, attrs):
        category = attrs.get("category")
        model = attrs.get("model")

        if model and category and model.category != category:
            raise serializers.ValidationError(
                "Модель не принадлежит выбранной категории!"
            )

        return attrs

    def create(self, validated_data):
        images_data = validated_data.pop("images", [])

        request = self.context.get("request")  

        product = Product.objects.create(
            user=request.user,
            **validated_data
        )

        for img in images_data:
            ProductImage.objects.create(product=product, image=img)

        return product
