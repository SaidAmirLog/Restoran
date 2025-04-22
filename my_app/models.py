from django.db import models
from users.models import User

# Create your models here.



class Table(models.Model):
    number = models.CharField(max_length=10)
    seats = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Столик {self.number} - {self.seats} мест"

class Dish(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='dishes/', blank=True, null=True)

    def __str__(self):
        return self.name

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    guests = models.PositiveIntegerField()
    table = models.ForeignKey('Table', on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField()
    time = models.TimeField()
    dishes = models.ManyToManyField('Dish', blank=True)

    def save(self, *args, **kwargs):
        if not self.table and self.guests <= 30:
            available_table = Table.objects.filter(is_available=True, seats__gte=self.guests).first()
            if available_table:
                self.table = available_table
                self.table.is_available = False
                self.table.save()
                print(f"Столик {self.table.number} был назначен.")
            else:
                print("Нет доступных столиков для такого количества гостей.")
        super().save(*args, **kwargs)
    def cancel(self):
        if self.table:
            self.table.is_available = True
            self.table.save()
        self.delete()
    def __str__(self):
        return f"Бронь для {self.user.username} на {self.date} в {self.time}"

class BookingReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(verbose_name="Отзыв")
    rating = models.PositiveSmallIntegerField(verbose_name="Оценка", choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"Отзыв от {self.user.username}"
