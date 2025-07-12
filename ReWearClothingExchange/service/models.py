from django.db import models

class Login(models.Model):
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    c_password = models.CharField(max_length=50)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Item(models.Model):
    SIZE_CHOICES = [
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Extra Extra Large'),
    ]

    CONDITION_CHOICES = [
        ('new', 'New'),
        ('like_new', 'Like New'),
        ('used', 'Used'),
    ]

    STATUS_CHOICES = [
        ('available', 'Available'),
        ('sold', 'Sold'),
        ('exchanged', 'Exchanged'),
    ]

    user = models.ForeignKey('Login', on_delete=models.CASCADE, related_name='items')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='items/', blank=True, null=True)
    size = models.CharField(max_length=5, choices=SIZE_CHOICES)
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.size})"


class UserDetails(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
