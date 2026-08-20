from django.db import models
from django.utils.safestring import mark_safe

# Create your models here.
Role=[
    ('1','Buyer'),
    ('2','Seller')
]
class Registration(models.Model):
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=25)
    password = models.CharField(max_length=16)
    phone = models.CharField(max_length=10)
    address = models.TextField()
    status = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    role =models.CharField(max_length=20,choices=Role)
    id_proof = models.ImageField(upload_to="photos/", blank=True)

    def proof(self):
        return mark_safe('<img src="{}" width="100"/>'.format(self.id_proof.url))

    def __str__(self):
        return self.name
class Category(models.Model):
    category_name=models.CharField(max_length=15)
    description=models.TextField()

    def __str__(self):
        return self.category_name


class Property(models.Model):
    category_id = models.ForeignKey(Category,on_delete=models.CASCADE)
    seller_id = models.ForeignKey(Registration,on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    description = models.TextField()
    type = models.CharField(max_length=15)
    location = models.CharField(max_length=40)
    price = models.CharField(max_length=10)
    status = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="property_images/")

    def __str__(self):
        return self.property.title

class Purchase(models.Model):
    property_id = models.ForeignKey(Property,on_delete=models.CASCADE)
    buyer_id = models.ForeignKey(Registration,on_delete=models.CASCADE)
    purchase_date = models.DateField(auto_now_add=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    amount = models.FloatField()
    payment_mode = models.CharField(max_length=15)
    ownership_transfer_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10)
    razorpay_payment_id = models.CharField(max_length=35)

    def __str__(self):
         return f"{self.buyer_id.name}"

class Payment(models.Model):
    purchase_id = models.ForeignKey(Purchase,on_delete=models.CASCADE)
    amount = models.FloatField(max_length=10)
    payment_date = models.DateField(auto_now_add=True)
    transaction_id = models.IntegerField()
    status = models.CharField(max_length=10)
    user_id = models.ForeignKey(Registration,on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.purchase_id.name}"
class Feedback(models.Model):
    buyer_id = models.ForeignKey(Registration,on_delete=models.CASCADE)
    property_id = models.ForeignKey(Property,on_delete=models.CASCADE)
    rating = models.CharField(max_length=5)
    comment = models.TextField()
    feedback_date = models.DateField(auto_now_add=True)
    def __str__(self):
        return f"{self.buyer_id.name}"


class Wishlist(models.Model):
    buyer_id = models.ForeignKey(Registration,on_delete=models.CASCADE)
    property_id = models.ForeignKey(Property,on_delete=models.CASCADE)
    added_date = models.DateField(auto_now_add=True)
    def __str__(self):
        return f"{self.buyer_id.name}"


class Customer_Support(models.Model):
    first_name=models.CharField(max_length=20,null=True,blank=True)
    last_name=models.CharField(max_length=20,null=True,blank=True)
    mobile_number=models.CharField(max_length=10,null=True,blank=True)
    email=models.EmailField(max_length=25,null=True,blank=True)
    query=models.TextField()
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.first_name
