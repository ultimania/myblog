from django.shortcuts import render
from django.views import generic
from .models import *
from .forms import *
from .utils import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib import messages

class BlogBaseView(generic.ListView):
    # 記事一覧画面をデフォルトとする
    # それ以外の画面のビューとして継承する際は適宜書き換えること
    model                   = TopicsTr
    namespace               = 'list'
    context_object_name     = 'model_data'
    template_name           = 'BlogManager/list.html'
    paginate_by             = 8
    extract_length          = 40

    def post(self, request, *args, **kwargs):
        if(self.namespace == 'search'):
            # 各ページからの検索ボタンによるPOST受付処理
            search_value = [self.request.POST.get('search_words', None),]
            request.session['search_words'] = search_value
            # 検索時にページネーションに関連したエラーを防ぐ
            self.request.GET = self.request.GET.copy()
            self.request.GET.clear()
            # GETリクエスト処理
            return self.get(request, *args, **kwargs)

    def get_queryset(self):
        # 検索条件の設定
        q_objects = Q(isdraft=False)
        order_by = '-created_at'
        if self.request.method == 'POST' and 'search_words' in self.request.session:
            # 検索フォームからのPOSTリクエストの場合はキーワード検索
            search_words = self.request.session['search_words']
            order_by = '-likes'
            for search_word in search_words:
                q_objects |= Q(text__contains=search_word)
        elif self.namespace == 'drafts':
            # 下書き一覧の場合は下書きフラグが立っているもの
            q_objects = Q(isdraft=True)
        else:
            pass
        # 指定した検索条件によるモデルデータの取得とダイジェスト抽出
        queryset = TopicsTr.objects.select_related().filter(q_objects).order_by(order_by)
        for query in queryset:
            query.text = extractDigest(query.text, self.extract_length)
            query.created_at = query.created_at.date()
        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ヘッダ情報の設定
        context['page_title'] = "feivs2019's blog | " + self.namespace
        context['keywords'] = "feivs2019,blog,Django,Python"
        count = len(self.get_queryset())
        # sessionに値がある場合、その値をセットする。（ページングしてもform値が変わらないように）
        search_words = self.request.session['search_words'][0] if 'search_words' in self.request.session else ''
        # Formオブジェクトの設定
        context['search_form'] = SearchForm(initial={'search_words': search_words,})
        context['upload_form'] = UploadForm()
        context['post_form'] = PostForm()
        context['comment_form'] = CommentForm()
        # コンテンツ情報の設定
        context['content_title'] = "記事一覧"
        context['digest_link'] = "blog:topic"
        # ホーム画面の場合はページングしない
        context['page_obj'] = None if self.namespace == 'home' else context['page_obj']
        return context


class UploadView(LoginRequiredMixin, generic.CreateView):
    """ファイルモデルのアップロードビュー POST専用"""
    model = MediaTr
    form_class = UploadForm
    success_url = reverse_lazy('blog:post')
    

class TopicView(BlogBaseView):
    template_name           = 'BlogManager/topic.html'
    namespace               = 'topic'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # URLのpkの価で一意な情報を取得する
        context['model_data'] = TopicsTr.objects.filter(id=self.kwargs['pk']).select_related().get()
        context['page_title'] = "feivs2019's blog | " + context['model_data'].title
        context['comments'] = CommentTr.objects.filter(topic=context['model_data'].id).order_by('-created_at')
        return context

    def post(self, request, *args, **kwargs):
        # コメント投稿処理
        data = {
            "topic"   : TopicsTr.objects.filter(id=self.kwargs['pk']).select_related().get()
            ,"author" : self.request.POST['author']
            ,"text" : self.request.POST['text']
        }
        CommentTr.objects.create(**data)
        # GETリクエスト処理
        return self.get(request, *args, **kwargs)
        

class TopicUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TopicsTr
    form_class = PostForm
    template_name = 'BlogManager/post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "feivs2019's blog | 記事を書く"
        context['keywords'] = "feivs2019,blog,Django,Python"
        # Formオブジェクトの設定
        search_words = self.request.session['search_words'][0] if 'search_words' in self.request.session else ''
        context['search_form'] = SearchForm(initial={'search_words': search_words,})
        context['upload_form'] = UploadForm()
        # コンテンツ情報の設定
        context['content_title'] = "記事を書く"
        return context

    def form_valid(self, form):
        result = super().form_valid(form)
        messages.success(
            self.request, '「{}」を更新しました'.format(form.instance))
        return result


class PostView(LoginRequiredMixin, generic.CreateView):
    model = TopicsTr
    form_class = PostForm
    context_object_name = 'model_data'
    template_name = 'BlogManager/post.html'
    success_url = "/blog/list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_form'] = PostForm()
        context['post_link'] = "blog:post"

        context['page_title'] = "feivs2019's blog | 記事を書く"
        context['keywords'] = "feivs2019,blog,Django,Python"
        # Formオブジェクトの設定
        search_words = self.request.session['search_words'][0] if 'search_words' in self.request.session else ''
        context['search_form'] = SearchForm(initial={'search_words': search_words,})
        context['upload_form'] = UploadForm()
        # コンテンツ情報の設定
        context['content_title'] = "記事を書く"
        return context



class DraftsView(LoginRequiredMixin, BlogBaseView):
    namespace               = 'drafts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['content_title'] = "下書き一覧"
        context['digest_link'] = "blog:update"

        return context


class HomeView(BlogBaseView):
    template_name = 'BlogManager/index.html'
    namespace               = 'home'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['content_title'] = "最新記事"
        return context


class SearchView(generic.ListView):
    namespace               = 'search'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['content_title'] = text + "を含む記事一覧 (全" + str(len(context['object'])) + "件)"
        return context

