from django.urls import path

from . import views

app_name = 'funTrip'
# urlpatterns = [
#     # name 引数を定義したので、テンプレートタグの {%url%} を使用して、
#     # URL 設定で定義されている特定の URL パスへの依存をなくすことができます:
#     path('', views.index, name='index'),
#     path('detail/<int:question_id>/', views.detail, name='detail'),
#     path('<int:question_id>/results/', views.results, name='results'),
#     path('<int:question_id>/votes/', views.votes, name='votes'),
# ]

urlpatterns = [
    # name 引数を定義したので、テンプレートタグの {%url%} を使用して、
    # URL 設定で定義されている特定の URL パスへの依存をなくすことができます:
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:pk>/votes/', views.votes, name='votes'),
]