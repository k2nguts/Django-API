from rest_framework import serializers
from .models import MenuItem
from decimal import Decimal
from .models import Category,Rating,Cart
from rest_framework.validators import UniqueValidator
from rest_framework.validators import UniqueTogetherValidator
import bleach
from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','slug','title']
        extra_kwargs = {
        'price' : {'min_value': 2},
        'stock' : {'source':'inventory','min_value': 0}     
        }
class MenuItemSerializer(serializers.HyperlinkedModelSerializer):
    stock = serializers.IntegerField(source = 'inventory', min_value = 0)
    price_after_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    category = CategorySerializer(read_only = True)
    category_id = serializers.IntegerField(write_only = True)
    title = serializers.CharField(
         max_length=255,
         validators=[UniqueValidator(queryset=MenuItem.objects.all())]
     )
    def validate(self, attrs):
     attrs['title'] = bleach.clean(attrs['title'])
     if(attrs['price']<2):
        raise serializers.ValidationError('Price should not be less than 2.0')
     if(attrs['inventory']<0):
         raise serializers.ValidationError('Stock cannot be negative')
     return super().validate(attrs)
    class Meta:
        model = MenuItem
        fields = ['id','title','price','stock','price_after_tax','category','category_id'] # 'stock','price_after_tax' 'category'#you can add stock instead of inventory
        extra_kwargs = {
         'price': {'min_value': 2}
         }
        
    def calculate_tax(self,product:MenuItem):
        return product.price * Decimal(1.1)
        
class RatingSerializer (serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset = User.objects.all(),
         default=serializers.CurrentUserDefault()
        )
    
    #serializers.PrimaryKeyRelatedField(
        #queryset = User.objects.all(),
        #default = serializers.CurrentUserDefault()
        #)
    class Meta:
        model =Rating
        fields = ['user','menuitem_id','rating']
        validators = [
            UniqueTogetherValidator(
            queryset= Rating.objects.all(),
            fields=['user','menuitem_id','rating']
        )
        ]
        extra_kwargs = {
                'rating': {'max_value':5,'min_value':0}
            }
class CartSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset = User.objects.all(),
         default=serializers.CurrentUserDefault()
        )
    class Meta:
        model = Cart
        fields=['user','menuitem_id','quantity']
        validators = [
            UniqueTogetherValidator(
                queryset=Cart.objects.all(),
                fields= ['user','menuitem_id','quantity']
            )
        ]
    extra_kwargs = {
         'quantity': {'min_value': 0} 
         }
        
        
#class MenuItemSerializer(serializers.Serializer):
    # id = serializers.IntegerField()
    #title=serializers.CharField(max_length=255)
    
