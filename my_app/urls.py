from django.urls import path
from . import views

urlpatterns = [
    path('reservation/create/', views.ReservationCreateView.as_view(), name='reservation_create'),
    path('my-reservations/', views.MyReservationsView.as_view(), name='my_reservations'),
    path('reserve/', views.ReservationCreateView.as_view(), name='reserve_table'),
    path('reserve/dishes/', views.ReservationCreateWithDishesView.as_view(), name='reservation_form'),
    path('reservation_success/', views.ReservationSuccessView.as_view(), name='reservation_success'),
    path('menu/', views.MenuView.as_view(), name='menu'),
    path('reviews/', views.ReviewListCreateView.as_view(), name='reviews'),
    path('contacts/', views.ContactView.as_view(), name='contacts'),
    path('dish/create/', views.DishCreateView.as_view(), name='create_dish'),
    path('dish/delete/<int:pk>/', views.DishDeleteView.as_view(), name='delete_dish'),
    path('reservation/cancel/<int:reservation_id>/', views.CancelReservationView.as_view(), name='cancel_reservation'),
]


