#from django.shortcuts import render
from rest_framework import generics
from .models import MenuItem,Rating,Category,Cart
from .serializers import MenuItemSerializer
from rest_framework.decorators import api_view ,renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer , StaticHTMLRenderer
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import CategorySerializer,RatingSerializer,CartSerializer
from django.core.paginator import Paginator,EmptyPage
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes,throttle_classes,action
from rest_framework.throttling import AnonRateThrottle
from rest_framework.throttling import UserRateThrottle
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User,Group
from rest_framework import permissions


class CartView(generics.ListCreateAPIView,generics.RetrieveUpdateAPIView,generics.DestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    def get_queryset(self):
        items = MenuItem.objects.select_related('category').all()
        queryset = MenuItem.objects.select_related('category').all()
        

class IsManagerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow managers to create objects.
    """

    def has_permission(self, request, view):
        # Allow GET, HEAD, or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Allow POST request only if user is a manager.
        return request.user.groups.filter(name='Manager').exists()      
        
    
class MenuItemsView(generics.ListCreateAPIView):

    queryset = MenuItem.objects.select_related('category').all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated, IsManagerOrReadOnly]

    
    def get_throttles(self):
        throttle_classes=[UserRateThrottle]
        if self.request.method == 'create':
            throttle_classes = [UserRateThrottle]
        else:
            throttle_classes = []
        return [throttle() for throttle in throttle_classes]
    def get_queryset(self):
        items = MenuItem.objects.select_related('category').all()
        queryset = MenuItem.objects.select_related('category').all()
        category_name = self.request.query_params.get('category')
        to_price = self.request.query_params.get('to_price')
        search = self.request.query_params.get('search')
        ordering = self.request.query_params.get('ordering')
        perpage = self.request.query_params.get('perpage',default = 2)
        page = self.request.query_params.get('page',default = 1)
        

        if category_name:
            queryset = queryset.filter(category__title=category_name)
        if to_price:
            queryset = queryset.filter(price=to_price)
        if search:
            queryset = queryset.filter(title__iscontains=search)
        if ordering :
            ordering_fields = ordering.split(",")
            queryset= queryset.order_by(*ordering_fields)
        paginator = Paginator(queryset,per_page=perpage)
        try:
            queryset = paginator.page(number=page)
        except EmptyPage:
            queryset = []
            
        return queryset
    
   
#api_view()
#def menuitems(request):
#    return Response('list of the books',status=status.HTTP_200_OK)

class SingleMenuItemView(generics.RetrieveUpdateAPIView,generics.DestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class=MenuItemSerializer
    permission_classes = [IsAuthenticated, IsManagerOrReadOnly]


@api_view()
def category_detail(request, pk):
 category = get_object_or_404(Category,pk=pk)
 serialized_category = CategorySerializer(category)
 return Response(serialized_category.data) 


class CategoryItemView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsManagerOrReadOnly]
    
    
@api_view() 
@renderer_classes([TemplateHTMLRenderer])
def menu(request):
 items = MenuItem.objects.select_related('category').all()
 serialized_item = MenuItemSerializer(items, many=True)
 return Response({'data':serialized_item.data}, template_name='menu-items.html')


@api_view(['GET'])
@renderer_classes([StaticHTMLRenderer])
def welcome(request):
    data = '<html><body><h1>Welcome To Little Lemon API Project</h1></body></html>'
    return Response(data)
@api_view()
@permission_classes({IsAuthenticated})
def secret(request):
    return Response({"message":"some secret message"})
@api_view()
@permission_classes({IsAuthenticated})
def manager_view(request):
    if request.user.groups.filter(name='Manager').exists():
        return Response({"message":"only manager can see this content"})
    else:
        return Response({"message":"you are not authorized"},403)
@api_view()    
@throttle_classes({AnonRateThrottle})
def throttle_check(request):
    return Response({"message":"successful"})

@api_view()    
@permission_classes({IsAuthenticated})
@throttle_classes({UserRateThrottle})
def throttle_check_auth(request):
    return Response({"message":"message for the logged in users only"})

@api_view(['POST'])    
@permission_classes(IsAdminUser)
def managers(request):
    username = request.data['username']
    if username:
        user = get_object_or_404(User,username=username)
        managers = Group.objects.get(name = "manager")
        if request.method == 'POST':
            managers.user_set.add(user)
        elif request.method == 'DELETE':
            managers.user_set.remove(user)
            
        return Response({"message":"ok"}) 
        
        
    return Response({"message":"error"},status.HTTP_400_BAD_REQUEST)

class RatingsView(generics.ListCreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    def get_permissions(self):
        if(self.request.method=='GET'):
            return []
        return [IsAuthenticated()]


class MenuItemViewAll(generics.ListCreateAPIView):
    queryset = MenuItem.objects.select_related('category').all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated, IsManagerOrReadOnly]
    
    def get_throttles(self):
        throttle_classes=[UserRateThrottle]
        if self.request.method == 'create':
            throttle_classes = [UserRateThrottle]
        else:
            throttle_classes = []
        return [throttle() for throttle in throttle_classes]
    def get_queryset(self):
        items = MenuItem.objects.select_related('category').all()
        queryset = MenuItem.objects.select_related('category').all()
        category_name = self.request.query_params.get('category')
        to_price = self.request.query_params.get('to_price')
        search = self.request.query_params.get('search')
        ordering = self.request.query_params.get('ordering')
        

        if category_name:
            queryset = queryset.filter(category__title=category_name)
        if to_price:
            queryset = queryset.filter(price=to_price)
        if search:
            queryset = queryset.filter(title__iscontains=search)
        if ordering :
            ordering_fields = ordering.split(",")
            queryset= queryset.order_by(*ordering_fields)
            

        return queryset