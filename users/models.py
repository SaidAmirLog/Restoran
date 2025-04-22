from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('customer', 'Клиент'),
        ('admin', 'Администратор'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.jpg')

    groups = models.ManyToManyField(Group, related_name="custom_user_set", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions_set", blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def save(self, *args, **kwargs):
        self.is_staff = self.role == 'admin'
        self.is_superuser = self.role == 'admin'
        super().save(*args, **kwargs)

    def is_admin(self):
        return self.role == 'admin'


class EmailVerificationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Restaurant(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название ресторана")
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(upload_to='restaurant/', verbose_name="Изображение", blank=True, null=True)

    def __str__(self):
        return self.name
class Dish(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="dishes")

    def __str__(self):
        return self.name


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reservations")
    date = models.DateField()
    time = models.TimeField()
    guests = models.PositiveIntegerField()
    dishes = models.ManyToManyField(Dish, blank=True, related_name="reservations")

    def __str__(self):
        return f"Бронь {self.user.username} на {self.date} в {self.time}"
