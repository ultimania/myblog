"""dashboard用views

    * ダッシュボードで使用する各ビューを定義
    * 各ビューは必ずBaseViewを継承すること

"""
from abc import ABCMeta, abstractmethod

from django.conf import settings
from django.shortcuts import render
from django.shortcuts import redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.template.loader import render_to_string
from django.db.models import Q
from django.urls import reverse_lazy
from django.http import Http404, HttpResponseBadRequest

from blogs.models import *
from .models import *
from .forms import *
from .config import *


class BaseView(LoginRequiredMixin, metaclass=ABCMeta):
    """BaseView
    
        各Viewクラスのスーパークラス

    Attributes:
        namespace (string): Template中でViewを識別するための文字列
        extract_length (int): 記事ダイジェストで表示させる文字数
        model (django.model): 対象モデルクラス 
        context_object_name (string): コンテキスト名
        template_name (string): テンプレートファイル名
        paginate_by (int): 1ページ当たりの表示数

    """
    namespace = 'Abstract'
    extract_length  = None
    model  = TopicsTr
    context_object_name = 'datas'
    template_name  = None
    paginate_by  = None
    login_url = '/dashboard/signin'
    redirect_field_name = 'redirect_to'

    def get_queryset(self):
        """get_querysetメソッド

        Args:
            request (request): 1st argument

        Returns:
            django.queryset: クエリセット
        
        Raises:
            none

        Vields:
            none
        
        Examples:
            >>> queryset = get_queryset()

        Note:
            未実装でスーパークラスのメソッドを呼び出す。

        """
        return self.model.objects.order_by('-created_at')

    def get_context_data(self, **kwargs):
        """get_context_dataメソッド

        Args:
            request (request): 1st argument

        Returns:
            django.queryset: クエリセット
        
        Raises:
            none

        Vields:
            none
        
        Examples:
            >>> context = get_context_data(kwargs)

        Note:
            未実装で以下のコンテキストを生成する
            * スーパークラスのコンテキスト
            * ページタイトル
            * ページキーワード
            * 検索フォーム
            * 投稿フォーム

        """
        context = super().get_context_data(**kwargs)
        context['page_title'] = Config.page_title + "：" + self.namespace
        context['keywords'] = Config.keywords
        context['namespace'] = self.namespace

        search_words = self.request.session['search_words'][0] if 'search_words' in self.request.session else ''
        context['SearchForm'] = SearchForm(initial={'search_words': search_words,})
        
        return context


class SigninView(LoginView):
    """SigninView
    
        サインイン用のビュー

    Attributes:
        form_class (forms.Form): SigninForm
        namespace (string): signin
        template_name (string): サインイン用テンプレート

    """
    form_class = SigninForm
    namespace = 'signin'
    template_name = 'dashboard/signin.html'


class SignupView(generic.CreateView):
    """SignupView
    
        サインイン用のビュー

    Attributes:
        form_class (forms.Form): SignupForm
        namespace (string): signup
        template_name (string): サインアップ用テンプレート

    """
    form_class = SignupForm
    namespace = 'signup'
    template_name = 'dashboard/signup.html'

    def form_valid(self, form):
        """form_validメソッド

        Args:
            form (forms.Form): 1st argument

        Returns:
            redirect('register:user_create_done')
        
        Raises:
            none

        Vields:
            none
        
        Examples:
            >>> form_valid(form)

        Note:
            仮登録と本登録用メールの発行

        """        
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': self.request.scheme,
            'domain': domain,
            'token': dumps(user.pk),
            'user': user,
        }

        subject = render_to_string('conf/mail_subject.txt', context)
        message = render_to_string('conf/mail_message.txt', context)

        user.email_user(subject, message)
        return redirect('dashboard:signup_done')

    def get_context_data(self, **kwargs):
        """get_context_dataメソッド

        Args:
            none

        Returns:
            context
        
        Raises:
            none

        Vields:
            none
        
        Examples:
            >>> get_context_data(**kwargs)

        Note:
            仮登録完了ページの表示テキストの定義

        """        
        context = super().get_context_data(**kwargs)
        context['page_title'] = "仮登録完了"
        context['panel-title'] = "仮登録が完了しました"
        context['message'] = "登録したメールアドレス宛に送ったURLにアクセスして本登録してください。"
        return context


class SignupDoneView(generic.base.TemplateView):
    """SignupDoneView
    
        サインアップ実施用のビュー

    Attributes:
        namespace (string): signup_done
        template_name (string): サインアップ実施用テンプレート

    """
    namespace = 'signup_done'
    template_name = 'dashboard/signup_done.html'

    def get_context_data(self, **kwargs):
        """get_context_dataメソッド

        Args:
            none

        Returns:
            context
        
        Raises:
            none

        Vields:
            none
        
        Examples:
            >>> get_context_data(**kwargs)

        Note:
            仮登録完了ページの表示テキストの定義

        """        
        context = super().get_context_data(**kwargs)
        context['page_title'] = "仮登録完了"
        context['panel_title'] = "仮登録が完了しました"
        context['message'] = "仮登録が完了しました。登録したアドレス宛に送ったメールを確認してください。"
        return context


class SignupCompleteView(generic.base.TemplateView):
    """SignupDoneView
    
        サインアップ完了用のビュー

    Attributes:
        namespace (string): signup_complete
        template_name (string): サインアップ完了用テンプレート

    """
    namespace = 'signup_complete'
    template_name = 'dashboard/signup_done.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)

    def get(self, request, **kwargs):
        """getメソッド

        Args:
            request (request): 1st argument

        Returns:
            super().get
            HttpResponseBadRequest()
        
        Raises:
            none

        Vields:
            none
        
        Examples:
            >>> context = get_context_data(kwargs)

        Note:
            　URLのトークンを確認して本登録を行う

        """        
        token = kwargs.get('token')
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoesNotExist:
                return HttpResponseBadRequest()
            else:
                if not user.is_active:
                    # 問題なければ本登録とする
                    user.is_active = True
                    user.save()
                    return super().get(request, **kwargs)

        return HttpResponseBadRequest()


    def get_context_data(self, **kwargs):
        """get_context_dataメソッド

        Args:
            none

        Returns:
            context
        
        Raises:
            none

        Vields:
            none
        
        Examples:
            >>> get_context_data(**kwargs)

        Note:
            本登録完了ページの表示テキストの定義

        """        
        context = super().get_context_data(**kwargs)
        context['page_title'] = "本登録完了"
        context['panel_title'] = "本登録が完了しました"
        context['message'] = "本登録が完了しました。登録した情報でサインインしてください。"
        return context


class SignoutView(BaseView, LogoutView):
    """SignoutView
    
        サインアウト用のビュー

    Attributes:
        namespace (string): signout
        template_name (string): サインアウト用テンプレート

    """
    namespace = 'signout'
    template_name = 'dashboard/signout.html'


class IndexView(BaseView, generic.ListView):
    """IndexView
    
        ダッシュボードトップ用のビュー

    Attributes:
        namespace (string): index
        model (django.model): AccessTr
        template_name (string): サインイン用テンプレート

    """
    namespace = 'index'
    template_name = 'dashboard/index.html'
    model = AccessTr

    def get_queryset(self):
        """get_querysetメソッド

        Args:
            request (request): 1st argument

        Returns:
            django.queryset: クエリセット
        
        Raises:
            none

        Vields:
            none
        
        Examples:
            >>> queryset = get_queryset()

        Note:
            未実装でスーパークラスのメソッドを呼び出す。

        """
        queryset = self.model.objects.all()
        return queryset


class ListView(BaseView, generic.ListView):
    """ListView

        記事の管理用のビュー

    Attributes:
        namespace (string): list
        template_name (string): list.html
        paginate_by (int): 8

    """
    namespace = 'list'
    template_name = 'dashboard/list.html'
    paginate_by = 8

    def get_queryset(self):
        """get_querysetメソッド

        Args:
            request (request): 1st argument

        Returns:
            django.queryset: クエリセット
        
        Raises:
            none

        Vields:
            none
        
        Examples:
            >>> queryset = get_queryset()

        Note:
            検索ワードがある場合は絞り込む

        """
        queryset = super().get_queryset()
        search_words = [self.request.GET.get('search_words', None),]
        if search_words:
            queryset = queryset.filter(
                Q(text__icontains=search_words)
            )
        return queryset

    def get_context_data(self, **kwargs):
        """get_context_dataメソッド

        Args:
            none

        Returns:
            django.context: コンテキスト
        
        Raises:
            none

        Vields:
            none
        
        Examples:
            >>> context = get_context_data()

        Note:
            モデルクラスからオブジェクトリストを生成する

        """
        self.object_list = self.model.objects.all()
        context = super().get_context_data(**kwargs)
        return context


class EditView(BaseView, generic.CreateView):
    """EditView

        記事を書く用のビュー

    Attributes:
        namespace (string): edit
        template_name (string): edit.html
        form_class (forms.Form) = TopicForm

    """
    namespace = 'edit'
    template_name = 'dashboard/edit.html'
    form_class = TopicForm
    success_url = reverse_lazy('dashboard:result')

    def get_queryset(self):
        """get_querysetメソッド

        Args:
            request (request): 1st argument

        Returns:
            django.queryset: クエリセット
        
        Raises:
            none

        Vields:
            none
        
        Examples:
            >>> queryset = get_queryset()

        Note:
            クエリパラメータに記事IDがある場合、
            該当の記事情報を取得する

        """
        queryset = super().get_queryset()
        if self.request.GET.get("entry"):
            queryset = queryset.get(id=self.request.GET.get("entry"))
        return queryset


class UpdateView(BaseView, generic.UpdateView):
    """EditView

        記事を書く用のビュー

    Attributes:
        namespace (string): edit
        template_name (string): edit.html
        form_class (forms.Form) = TopicForm

    """
    namespace = 'update'
    template_name = 'dashboard/edit.html'
    form_class = TopicForm
    success_url = reverse_lazy('dashboard:result')


class ResultView(BaseView, generic.base.TemplateView):
    """EditView

        記事を書く用のビュー

    Attributes:
        namespace (string): edit
        template_name (string): edit.html
        form_class (forms.Form) = TopicForm

    """
    namespace = 'result'
    template_name = 'dashboard/result.html'
    form_class = TopicForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topic_id'] = "87159e8c-3943-4334-a3ec-f95615ae71a9"
        # context['topic_id'] = self.request.GET.get('topic_id')
        return context


class DeleteView(BaseView, generic.DeleteView):
    """DeleteView

        記事削除用のビュー

    Attributes:
        namespace (string): edit
        template_name (string): edit.html
        form_class (forms.Form) = TopicForm

    """
    namespace = 'delete'
    success_url = reverse_lazy('dashboard:list')

