from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Dish, BookingReview
from .forms import ReservationForm, DishForm, BookingReviewForm
from django.views.generic import *
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import DeleteView
from django.shortcuts import get_object_or_404
from .models import Reservation
from django.views.generic.edit import FormMixin

class ReservationCreateView(CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'main/reserve_table.html'
    success_url = reverse_lazy('reservation_success')

    def form_valid(self, form):
        guests = form.cleaned_data['guests']
        if guests > 30:
            messages.error(self.request, "Один столик вмещает максимум 30 человек.")
            return redirect('reserve_table')

        form.instance.user = self.request.user
        response = super().form_valid(form)

        selected_dishes_str = self.request.POST.get('selected_dishes', '')
        dish_ids = [int(i) for i in selected_dishes_str.split(',') if i.isdigit()]
        dishes = Dish.objects.filter(id__in=dish_ids)
        self.object.dishes.set(dishes)
        return response


class ReservationCreateWithDishesView(CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'main/reservation_form.html'
    success_url = reverse_lazy('reservation_success')

    def form_valid(self, form):
        form.instance.user = self.request.user

        if not form.instance.table:
            table = Table.objects.filter(seats__gte=form.instance.guests, is_available=True).first()
            if table:
                table.is_available = False
                table.save()
                form.instance.table = table

        response = super().form_valid(form)

        selected_dishes_str = self.request.POST.get('selected_dishes', '')
        dish_ids = [int(i) for i in selected_dishes_str.split(',') if i.isdigit()]
        dishes = Dish.objects.filter(id__in=dish_ids)
        self.object.dishes.set(dishes)

        return response



class ReservationSuccessView(TemplateView):
    template_name = 'main/reservation_success.html'


class MenuView(ListView):
    model = Dish
    template_name = 'main/menu.html'
    context_object_name = 'dishes'

    def get_queryset(self):
        return Dish.objects.all()


class ReviewListCreateView(FormMixin, ListView):
    model = BookingReview
    template_name = 'main/reviews.html'
    context_object_name = 'reviews'
    form_class = BookingReviewForm
    success_url = reverse_lazy('reviews')

    def get_queryset(self):
        return BookingReview.objects.all().order_by('-created_at')

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        form = self.get_form()
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return self.form_valid(form)
        return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context



class ContactView(TemplateView):
    template_name = 'main/contacts.html'


class DishCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Dish
    form_class = DishForm
    template_name = 'main/create_dish.html'
    success_url = reverse_lazy('menu')

    def test_func(self):
        return self.request.user.is_admin


class DishDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Dish
    template_name = 'main/delete_dish_confirm.html'
    success_url = reverse_lazy('menu')

    def test_func(self):
        return self.request.user.is_admin


class MyReservationsView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = 'main/my_reservations.html'
    context_object_name = 'reservations'

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user).order_by('-date', '-time')


class FeedbackView(LoginRequiredMixin, CreateView):
    model = BookingReview
    form_class = BookingReviewForm
    template_name = 'main/feedback.html'

    def get_success_url(self):
        return reverse_lazy('my_reservations')

    def form_valid(self, form):
        reservation = get_object_or_404(Reservation, id=self.kwargs['reservation_id'])
        if reservation.user != self.request.user:
            return redirect('my_reservations')

        form.instance.user = self.request.user
        form.instance.reservation = reservation
        return super().form_valid(form)





class CancelReservationView(DeleteView):
    model = Reservation
    template_name = 'main/confirm_cancel_reservation.html'
    context_object_name = 'reservation'

    def get_object(self):
        reservation = get_object_or_404(Reservation, id=self.kwargs['reservation_id'], user=self.request.user)
        return reservation

    def delete(self, request, *args, **kwargs):
        reservation = self.get_object()
        if reservation.table:
            reservation.table.is_available = True
            reservation.table.save()

        response = super().delete(request, *args, **kwargs)

        messages.success(request, "Ваше бронирование успешно отменено.")

        return response

    def get_success_url(self):
        return reverse_lazy('my_reservations')
