from django.contrib import admin
from .models import Question, Choice

# Register your models here.

class ChoiceInline(admin.TabularInline): # admin.StackedInlineと違いよりコンパクトに表示ができる
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fields = ['pub_date', 'question_text'] # 順番を固定する
    inlines = [ChoiceInline] # choiceをQuestionの中で表示させる
    list_display = ('pub_date', 'question_text', 'was_published_recently') # チェンジリストに表示するフィールドを決める
    list_filter = ['pub_date'] # フィルター機能を追加
    search_fields = ['question_text'] # 検索昨日を追加　Likeクエリで曖昧検索をしている
    list_per_page = 3 # ページ分割機能

# class QuestionAdmin(admin.ModelAdmin):
# 複数のフィールドで分割することもできる
#     fieldsets = [
    #     (None,               {'fields': ['question_text']}),
    #     ('Date information', {'fields': ['pub_date']}),
    # ]

admin.site.register(Question, QuestionAdmin)
# admin.site.register(Choice)