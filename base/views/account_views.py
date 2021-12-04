from django.urls.base import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin   # ログインしていなければ見れない
from django.contrib.auth import get_user_model
from django.contrib import messages
from base.models import Profile
from base.forms import UserCreationForm


class SignUpView(CreateView):
    template_name = 'pages/login_signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, '新規登録が完了しました。続けてログインしてください。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'エラーです。')
        return super().form_invalid(form)

class Login(LoginView):
    template_name = 'pages/login_signup.html'

    def form_valid(self, form):
        messages.success(self.request, 'ログインしました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'エラーでログインできません。')
        return super().form_invalid(form)

class AccountUpdateView(LoginRequiredMixin, UpdateView):    # 継承順は、LoginRequiredMixinsを先にする！！
    model = get_user_model()
    template_name = 'pages/account.html'
    fields = ['username', 'email',]
    success_url = reverse_lazy('top')

    # どのユーザーの情報を更新するか明確にするため、get_object()をオーバーライドし、pkを取得
    def get_object(self):
        # URL変数ではなく、現在のユーザーから直接pkを取得(あくまで、urlはaccount/のみでuser.idは不要)
        self.kwargs['pk'] = self.request.user.pk
        return super().get_object()

class ProfileUpdateView(LoginRequiredMixin, UpdateView):    # LoginRequiredMixinを先にする
    model = Profile
    template_name = 'pages/profile.html'
    fields = ['name', 'zipcode', 'prefecture', 'city', 'address1', 'address2', 'tel']
    success_url = reverse_lazy('top')

    def get_object(self):
        # URL変数ではなく、現在のユーザーから直接pkを取得
        self.kwargs['pk'] = self.request.user.pk
        return super().get_object()
