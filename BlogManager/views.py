from django.shortcuts import render
from django.views import generic
from .models import TopicsTr
from .forms import SearchForm

class HomeView(generic.ListView):
    model = ''
    context_object_name = 'model_data'
    template_name = 'BlogManager/index.html'
    get_count = 10
    # paginate_by = 30


    def get_queryset(self):
        queryset = TopicsTr.objects.select_related().all().order_by('-created_at')[:self.get_count]
        # for query in queryset:
            # query.text = extractDigest(query.text)
        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "feivs2019's blog"
        context['keywords'] = "feivs2019,blog,Django,Python"

        default_data = {
                        'search_words': '', 
                        }
        search_form = SearchForm(initial=default_data)
        context['search_form'] = search_form

        return context


class SearchView(generic.ListView):

    def get_queryset(self):
        # sessionに値がある場合、その値でクエリ発行する。
        if 'search_value' in self.request.session:
            search_value = self.request.session['search_value']
            title = search_value[0]
            text = search_value[1]
            # 検索条件
            condition_title = Q()
            condition_text = Q()
            if len(title) != 0 and title[0]:
                condition_title = Q(title__icontains=title)
            if len(text) != 0 and text[0]:
                condition_text = Q(text__contains=text)
            return Post.objects.select_related().filter(condition_title & condition_text)
        else:
            # 何も返さない
            return Post.objects.none()

        queryset = TopicsTr.objects.select_related().all().order_by('-post_timestamp')[:self.get_count]
        return queryset


    def post(self, request, *args, **kwargs):
        # 各ページからの検索ボタンによるPOST受付処理
        search_value = [
            self.request.POST.get('search_words', None),
        ]
        request.session['search_value'] = search_value
        # 検索時にページネーションに関連したエラーを防ぐ
        self.request.GET = self.request.GET.copy()
        self.request.GET.clear()
        # GETリクエスト処理
        return self.get(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "feivs2019's blog"
        context['keywords'] = "feivs2019,blog,Django,Python"

        # sessionに値がある場合、その値をセットする。（ページングしてもform値が変わらないように）
        text = ''
        if 'search_value' in self.request.session:
            search_value = self.request.session['search_value']
            text = search_value[0]
        default_data = {'search_words': search_words,}
        test_form = SearchForm(initial=default_data)
        context['test_form'] = test_form

        return context