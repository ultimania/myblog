from django.shortcuts import render
from django.views import generic
from .models import TopicsTr
from .forms import SearchForm
from .utils import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

class DraftsView(LoginRequiredMixin, generic.ListView):
# class DraftsView(generic.ListView):
    model = TopicsTr
    context_object_name = 'model_data'
    template_name = 'BlogManager/list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = TopicsTr.objects.select_related().filter(isdraft=True).order_by('-created_at')
        # 記事ダイジェストの取得
        for query in queryset:
            query.text = extractDigest(query.text, 40)
            query.created_at = query.created_at.date()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "feivs2019's blog | 下書き一覧"
        context['keywords'] = "feivs2019,blog,Django,Python"
        context['content_title'] = "下書き一覧"

        default_data = {
                        'search_words': '', 
                        }
        search_form = SearchForm(initial=default_data)
        context['search_form'] = search_form

        return context


class ListView(generic.ListView):
    model = TopicsTr
    context_object_name = 'model_data'
    template_name = 'BlogManager/list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = TopicsTr.objects.select_related().filter(isdraft=False).order_by('-created_at')
        # 記事ダイジェストの取得
        for query in queryset:
            query.text = extractDigest(query.text, 40)
            query.created_at = query.created_at.date()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "feivs2019's blog | 記事一覧"
        context['keywords'] = "feivs2019,blog,Django,Python"
        context['content_title'] = "記事一覧"

        default_data = {
                        'search_words': '', 
                        }
        search_form = SearchForm(initial=default_data)
        context['search_form'] = search_form

        return context


class HomeView(generic.ListView):
    model = TopicsTr
    context_object_name = 'model_data'
    template_name = 'BlogManager/index.html'
    get_count = 9
    # paginate_by = 30

    def get_queryset(self):
        queryset = TopicsTr.objects.select_related().all().order_by('-created_at')[:self.get_count]
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "feivs2019's blog"
        context['keywords'] = "feivs2019,blog,Django,Python"
        context['content_title'] = "最新記事"

        # 記事ダイジェストの取得
        digests = []
        for query in self.get_queryset():
            digests.append({
                'title'         : query.title
                ,'text'          : extractDigest(query.text, 40)
                ,'created_at'    : query.created_at.date()
                ,'likes'         : query.likes
            })
        context['digests'] = digests

        default_data = {
                        'search_words': '', 
                        }
        search_form = SearchForm(initial=default_data)
        context['search_form'] = search_form

        return context


class SearchView(generic.ListView):
    model = TopicsTr
    context_object_name = 'model_data'
    template_name = 'BlogManager/list.html'
    get_count = 9
    paginate_by = 10

    def get_queryset(self):
        # sessionに値がある場合、その値でクエリ発行する。
        if 'search_words' in self.request.session:
            search_words = self.request.session['search_words']
            text = search_words[0]
            # 検索条件
            condition_text = Q()
            if len(text) != 0 and text[0]:
                condition_text = Q(text__contains=text)
            # 記事ダイジェストの取得
            queryset = TopicsTr.objects.select_related().filter(condition_text).filter(isdraft=False).order_by('-likes')
            for query in queryset:
                query.text = extractDigest(query.text, 40)
                query.created_at = query.created_at.date()
            return queryset
        else:
            # 何も返さない
            return TopicsTr.objects.none()


    def post(self, request, *args, **kwargs):
        # 各ページからの検索ボタンによるPOST受付処理
        search_value = [
            self.request.POST.get('search_words', None),
        ]
        request.session['search_words'] = search_value
        # 検索時にページネーションに関連したエラーを防ぐ
        self.request.GET = self.request.GET.copy()
        self.request.GET.clear()
        # GETリクエスト処理
        return self.get(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "feivs2019's blog | 検索結果"
        context['keywords'] = "feivs2019,blog,Django,Python"
        count = len(self.get_queryset())

        # sessionに値がある場合、その値をセットする。（ページングしてもform値が変わらないように）
        if 'search_words' in self.request.session:
            search_words = self.request.session['search_words']
            text = search_words[0]
        default_data = {'search_words': text,}
        search_form = SearchForm(initial=default_data)
        context['search_form'] = search_form
        context['content_title'] = text + "を含む記事一覧 (全" + str(count) + "件)"

        return context