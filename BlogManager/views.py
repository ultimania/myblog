from .models import *
from .forms import *
from .utils import *

from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib import messages

'''===================================================
    BlogBaseViewクラス
        親クラス: generic.ListView
        urlマップ: blog:list
==================================================='''
class BlogBaseView(generic.ListView):
    # 記事一覧画面をデフォルトとする
    # それ以外の画面のビューとして継承する際は適宜書き換えること
    model                   = TopicsTr
    namespace               = 'list'
    context_object_name     = 'topics'
    template_name           = 'BlogManager/list.html'
    paginate_by             = 8
    extract_length          = 40

    def get_queryset(self):
        # フィルタリング条件の設定
        q_objects = Q(isdraft=False)
        order_by = '-created_at'
        if self.request.method == 'POST' and 'search_words' in self.request.session:
            # 検索フォームからのPOSTリクエストの場合はキーワード検索
            search_words = self.request.session['search_words']
            order_by = '-likes'
            for search_word in search_words:
                q_objects |= Q(text__contains=search_word)
        elif self.namespace == 'drafts':
            # 下書き一覧の場合は下書きフラグが立っているものを対象
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
        # 共通設定の取得
        get_common_data(self, context)
        # コンテンツ情報の設定
        context['content_title'] = "記事一覧"
        context['digest_link'] = "blog:topic"
        # ホーム画面の場合はページングしない
        context['page_obj'] = None if self.namespace == 'home' else context['page_obj']
        return context


'''===================================================
    UploadViewクラス
        親クラス: LoginRequiredMixin
                   generic.CreateView
        urlマップ: blog:upload
==================================================='''
class UploadView(LoginRequiredMixin, generic.CreateView):
    """ファイルモデルのアップロードビュー POST専用"""
    model = MediaTr
    form_class = UploadForm
    success_url = reverse_lazy('blog:post')
    

'''===================================================
    DraftsViewクラス
        親クラス: LoginRequiredMixin
                 BlogBaseView
        urlマップ: blog:drafts
==================================================='''
class DraftsView(LoginRequiredMixin, BlogBaseView):
    namespace               = 'drafts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # コンテンツ情報の設定
        context['content_title'] = "下書き一覧"
        context['digest_link'] = "blog:update"
        return context


'''===================================================
    HomeViewクラス
        親クラス: BlogBaseView
        urlマップ: blog:home
==================================================='''
class HomeView(BlogBaseView):
    template_name = 'BlogManager/index.html'
    namespace               = 'home'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['content_title'] = "最新記事"
        return context


'''===================================================
    SearchViewクラス
        親クラス: BlogBaseView
        urlマップ: blog:search
==================================================='''
class SearchView(BlogBaseView):
    namespace               = 'search'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['content_title'] = " ".join(context['search_words']) + "を含む記事一覧 (全" + str(len(context['object_list'])) + "件)"
        return context

    def post(self, request, *args, **kwargs):
        # 検索時にページネーションに関連したエラーを防ぐ
        self.request.GET = self.request.GET.copy()
        self.request.GET.clear()
        # GETリクエスト処理
        return self.get(request, *args, **kwargs)


'''===================================================
    TopicViewクラス
        親クラス: BlogBaseView
        urlマップ: blog:topic
==================================================='''
class TopicView(BlogBaseView):
    template_name           = 'BlogManager/topic.html'
    namespace               = 'topic'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # URLのpkの価で一意な情報を取得する
        context['topic'] = TopicsTr.objects.filter(id=self.kwargs['pk']).select_related().get()
        context['page_title'] = "feivs2019's blog | " + context['model_data'].title
        # topicに紐付くコメント情報を取得
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
        

'''===================================================
    PostFormViewクラス
        親クラス: LoginRequiredMixin
                 generic.CreateView
        urlマップ: blog:topic
==================================================='''
class PostFormView(LoginRequiredMixin, generic.FormView):
    model = TopicsTr
    form_class = PostForm
    template_name = 'BlogManager/post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 共通設定の取得
        get_common_data(self, context)
        # コンテンツ情報の設定
        context['content_title'] = "記事を書く"
        return context

    def form_valid(self, form):
        # 保存種別によってフラグを変える
        if self.request.POST.get('save_flg') == 'draft':
            self.object.isdraft = True
            result_message = '記事を下書き保存しました'
        else:
            self.object.isdraft = False
            result_message = '記事を更新しました'
        result = super().form_valid(form)
        messages.success(
            self.request, result_message.format(form.instance))
        return result


'''===================================================
    PostFormViewクラス
        親クラス: PostFormView
                 generic.CreateView
        urlマップ: blog:post
==================================================='''
class PostView(PostFormView, generic.CreateView):
    namespace               = 'post'


'''===================================================
    TopicUpdateViewクラス
        親クラス: PostFormView
                 generic.UpdateView
        urlマップ: blog:update
==================================================='''
class TopicUpdateView(PostFormView, generic.UpdateView):
    namespace               = 'update'

