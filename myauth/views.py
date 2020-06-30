from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views import generic
from .forms import LoginForm
from blogs.forms import SearchForm

class Login(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'registration/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'search_form': SearchForm,
        })
        return context


class Logout(LoginRequiredMixin, LogoutView):
    """ログアウトページ"""
    form_class = LoginForm
    template_name = 'registration/logout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'search_form': SearchForm,
        })
        return context
