from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.urls import reverse
from .models import Question, Choice
from django.views import generic
from django.utils import timezone

"""
汎用ビューを使うことで少ないコードで表現できる
"""
class IndexView(generic.ListView):
    template_name = 'funTrip/index.html'
    context_object_name = 'latest_question_list'
    
    def get_queryset(self) -> object:
        """最新の5つの質問を表示する"""
        # Question.objects.filter(pub_date__lte=timezone.now()) は、
        # pub_date が timezone.now 以前の Question を含んだクエリセットを返します。
        return Question.objects.filter(
            pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
    
class DetailView(generic.DetailView):
    model = Question
    template_name = 'funTrip/detail.html'
    def get_queryset(self) -> object:
        """
        Index.htmlで条件を満たさない質問を表示しないようにできるが
        推測されて表示してない質問のURLにたどり着く可能性があるので制御をする
        """
        # Question.objects.filter(pub_date__lte=timezone.now()) は、
        # pub_date が timezone.now 以前の Question を含んだクエリセットを返します。
        return Question.objects.filter(
            pub_date__lte=timezone.now())
    
class ResultsView(generic.DetailView):
    model = Question
    template_name = 'funTrip/results.html'
    def get_queryset(self) -> object:
        """
        Index.htmlで条件を満たさない質問を表示しないようにできるが
        推測されて表示してない質問のURLにたどり着く可能性があるので制御をする
        """
        # Question.objects.filter(pub_date__lte=timezone.now()) は、
        # pub_date が timezone.now 以前の Question を含んだクエリセットを返します。
        return Question.objects.filter(
            pub_date__lte=timezone.now())



"""
関数定義することで細かい処理のコードを実現できる
"""
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # template = loader.get_template('funTrip/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    # return HttpResponse(template.render(context, request))
    # htmlを読み込んで辞書を反映するをrenderだけですることができる
    return render(request, 'funTrip/index.html', context)

def detail(request, question_id):
    """try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")"""
    # 下記でtry exceptなしで1行で処理を書くことができる
    """
    第1引数 : djangoモデル
    任意の数のキーワード引数を取る : e.x. idなど
    
    オブジェクトが存在しない場合はにはHttp404を返します。
    """
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'funTrip/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'funTrip/results.html', {'question': question})

def votes(request, pk):
    question = get_object_or_404(Question, pk=pk)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice']) # request.POST[]は常に文字列を返す
    except (KeyError, Choice.DoesNotExist):
        # 再度質問票を表示する
        return render(request, 'funTrip/detail.html', {
            'question': question,
            'error_message': 'You did not select a choice'
        })
    else: # 正常終了時の処理
        selected_choice.votes += 1
        selected_choice.save()
        """
        ポスト処理に成功した後は必ず、HttpResponseRedirect する
        これは2回ポストをされるのを防ぐことができる。
        ウェブサイトにおけるリダイレクトとは、ウェブサイトの閲覧において、指定したウェブページから自動的に他のウェブページに転送されること
        """
        return HttpResponseRedirect(reverse('funTrip:results', args=(pk,))) # reversを使うことでURLのハードコードを防いでいる