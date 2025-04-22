from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, UpdateView, TemplateView, ListView
from .models import User, EmailVerificationCode, Reservation, Restaurant
from .forms import RegisterForm, LoginForm, VerifyEmailForm, ReservationForm
import random
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


def generate_verification_code():
    return str(random.randint(100000, 999999))


class HomeView(ListView):
    model = Restaurant
    template_name = 'main/base.html'
    context_object_name = 'restaurants'
    queryset = Restaurant.objects.all()[:1]
class RegisterView(FormView):
    template_name = 'users/register.html'
    form_class = RegisterForm

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.set_password(form.cleaned_data['password'])
        user.save()

        code = generate_verification_code()
        EmailVerificationCode.objects.create(user=user, code=code)

        send_mail(
            'Код подтверждения',
            f'Ваш код: {code}',
            'noreply@restaurant.com',
            [user.email]
        )

        return redirect('verify_email', user_id=user.id)


class VerifyEmailView(View):
    template_name = 'users/verify_email.html'

    def get(self, request, user_id):
        form = VerifyEmailForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, user_id):
        form = VerifyEmailForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            user = get_object_or_404(User, id=user_id)
            verification = EmailVerificationCode.objects.filter(user=user, code=code).first()

            if verification:
                user.is_active = True
                user.save()
                login(request, user)
                return redirect('home')

        return render(request, self.template_name, {'form': form, 'error': 'Неверный код'})


class LoginUserView(LoginView):
    template_name = 'users/login.html'
    form_class = LoginForm

    def form_valid(self, form):
        user = form.get_user()
        if user.is_active:
            login(self.request, user)
            return redirect('profile')
        return self.form_invalid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        email = user.email

        if email and "@" in email:
            name_part, domain = email.split("@")
            masked_name = "****" + name_part[4:] if len(name_part) > 4 else "****"
            masked_email = f"{masked_name}@{domain}"
        else:
            masked_email = ""

        context.update({
            'user': user,
            'masked_email': masked_email
        })
        return context




class EditProfileView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['username', 'email', 'avatar']
    template_name = 'users/edit_profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user


class ChangePasswordView(LoginRequiredMixin, FormView):
    template_name = 'users/new_password.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('profile')

    def get_form(self, form_class=None):
        return self.form_class(self.request.user, **self.get_form_kwargs())

    def form_valid(self, form):
        user = form.save()
        update_session_auth_hash(self.request, user)
        return super().form_valid(form)


class ReservationView(LoginRequiredMixin, FormView):
    template_name = 'users/reservation.html'
    form_class = ReservationForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        reservation = form.save(commit=False)
        reservation.user = self.request.user
        reservation.save()
        form.save_m2m()
        return super().form_valid(form)
