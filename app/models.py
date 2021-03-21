from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
DISTRICT_CHOICES = (
    ('Bagerhat', 'Bagerhat'),
    ('Bandarban', 'Bandarban'),
    ('Barisal', 'Barisal'),
    ('Bhola', 'Bhola'),
    ('Bogra', 'Bogra'),
    ('Brahmanbaria', 'Brahmanbaria'),
    ('Chandpur', 'Chandpur'),
    ('Chittagong', 'Chittagong'),
    ('Chuadanga', 'Chuadanga'),
    ('Comilla', 'Comilla'),
    ('Coxs Bazar', 'Coxs Bazar'),
    ('Dhaka', 'Dhaka'),
    ('Dinajpur', 'Dinajpur'),
    ('Faridpur', 'Faridpur'),
    ('Feni', 'Feni'),
    ('Gaibandha', 'Gaibandha'),
    ('Gazipur', 'Gazipur'),
    ('Gopalganj', 'Gopalganj'),
    ('Habiganj', 'Habiganj'),
    ('Jaipurhat', 'Jaipurhat'),
    ('Jamalpur', 'Jamalpur'),
    ('Jessore', 'Jessore'),
    ('Jhalakati', 'Jhalakati'),
    ('Jhenaidah', 'Jhenaidah'),
    ('Khagrachari', 'Khagrachari'),
    ('Khulna', 'Khulna'),
    ('Kishoreganj', 'Kishoreganj'),
    ('Kurigram', 'Kurigram'),
    ('Kushtia', 'Kushtia'),
    ('Lakshmipur', 'Lakshmipur'),
    ('Lalmonirhat', 'Lalmonirhat'),
    ('Madaripur', 'Madaripur'),
    ('Magura', 'Magura'),
    ('Manikganj', 'Manikganj'),
    ('Meherpur', 'Meherpur'),
    ('Moulvibazar', 'Moulvibazar'),
    ('Munshiganj', 'Munshiganj'),
    ('Mymensingh', 'Mymensingh'),
    ('Naogaon', 'Naogaon'),
    ('Narail', 'Narail'),
    ('Narayanganj', 'Narayanganj'),
    ('Narsingdi', 'Narsingdi'),
    ('Natore', 'Natore'),
    ('Nawabganj', 'Nawabganj'),
    ('Netrakona', 'Netrakona'),
    ('Nilphamari', 'Nilphamari'),
    ('Noakhali', 'Noakhali'),
    ('Pabna', 'Pabna'),
    ('Panchagarh', 'Panchagarh'),
    ('Parbattya Chattagram', 'Parbattya Chattagram'),
    ('Patuakhali', 'Patuakhali'),
    ('Pirojpur', 'Pirojpur'),
    ('Rajbari', 'Rajbari'),
    ('Rajshahi', 'Rajshahi'),
    ('Rangpur', 'Rangpur'),
    ('Satkhira', 'Satkhira'),
    ('Shariatpur', 'Shariatpur'),
    ('Sherpur', 'Sherpur'),
    ('Sirajganj', 'Sirajganj'),
    ('Sunamganj', 'Sunamganj'),
    ('Sylhet', 'Sylhet'),
    ('Tangail', 'Tangail'),
    ('Thakurgaon', 'Thakurgaon'),
)
class Customer(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    address=models.CharField(max_length=200) #address
    area=models.CharField(max_length=100) #area
    mobno=models.IntegerField() #mobno
    district=models.CharField(choices=DISTRICT_CHOICES,max_length=50) #area
    
    def __str__(self):
        return str(self.id)

CATEGORY_CHOICES=(
    ('M','Mobile'),
    ('L','Laptop'),
    ('TW','Top Wear'),
    ('BW','Bottom Wear'),
    ('W','Watch'),
)

class Product(models.Model):
    title=models.CharField(max_length=100)
    selling_price=models.FloatField()
    discounted_price=models.FloatField()
    description=models.TextField()
    brand=models.CharField(max_length=100)
    category=models.CharField(choices=CATEGORY_CHOICES,max_length=2)
    product_image=models.ImageField(upload_to='productimg')

    def __str__(self):
        return str(self.id)

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
    
    @property
    def total_cost(self):
        return self.quantity*self.product.discounted_price


STATUS_CHOICES=(
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel'),
)

class OrderPlaced(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    ordered_date=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=50,choices=STATUS_CHOICES,default='Pending')

    
    @property
    def total_cost(self):
        return self.quantity*self.product.discounted_price
