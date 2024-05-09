from django.db import models
from django.contrib.auth.models import User 

class Category(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return self.title
    
class Rating(models.Model):
    menuitem_id = models.ForeignKey('MenuItem',on_delete=models.CASCADE)
    rating = models.SmallIntegerField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)    
class MenuItem(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6 , decimal_places=2)
    inventory = models.IntegerField()
    #default_category = category.objects.get(id=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,default=1)  
    #above this line for the all menu items can delete for category class can deletiable
class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    delivery_crew = models.ForeignKey(User,on_delete=models.SET_NULL,related_name="delivery_crew",null = True)
    status = models.BooleanField(db_index=True,default=0)
    total = models.DecimalField(max_digits=6,decimal_places=2)
    date = models.DateField(db_index=True) 
    

class OrderItem(models.Model):
    order = models.ForeignKey(User,on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem,on_delete=models.CASCADE,related_name='order_items')
    quantity = models.SmallIntegerField()
    unitprice = models.DecimalField(max_digits=6,decimal_places=2)
    price = models.ForeignKey(MenuItem,on_delete=models.CASCADE)
    
class Meta:
        unique_together = ('order','menuitem')    
 
class Cart(models.Model):
    
    menuitem_id = models.ForeignKey(MenuItem,on_delete=models.CASCADE,related_name='cart_items')
    quantity = models.SmallIntegerField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    unitprice = models.DecimalField(max_digits=6,decimal_places=2,default=2)
    price = models.DecimalField(max_digits=6, decimal_places=2,default=0)
 
    class Meta:
        unique_together = ('menuitem_id','user')
    def clean(self):
        MenuItem = self.menuitem_id
        if self.quantity > MenuItem.inventory:
            raise ValueError("Requested quantity exceeds available inventory")

    def save(self, *args, **kwargs):
        self.clean()  # Ensure quantity does not exceed inventory before saving
        super().save(*args, **kwargs)