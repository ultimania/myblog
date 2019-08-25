from .forms import *

def extractDigest(text, count):
    # 先頭からcountの数だけ抽出
    result = text[0:count] + "..."
    return result

def get_common_data(instance, context):
    # ヘッダ情報の設定
    context['page_title'] = "feivs2019's blog | " + instance.namespace
    context['keywords'] = "feivs2019,blog,Django,Python"
    count = len(instance.get_queryset())
    # sessionに値がある場合、その値をセットする。（ページングしてもform値が変わらないように）
    context['search_words'] = instance.request.session['search_words'][0] if 'search_words' in instance.request.session else ''
    # Formオブジェクトの設定
    context['search_form'] = SearchForm(initial={'search_words': context['search_words'],})
    context['upload_form'] = UploadForm()
    context['post_form'] = PostForm()
    context['comment_form'] = CommentForm()
   