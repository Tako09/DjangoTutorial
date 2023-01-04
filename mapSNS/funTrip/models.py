import datetime
from django.db import models
from django.utils import timezone
from django.contrib import admin

# Create your models here.
# データベースの取る情報を明記する

"""
各フィールドは Field クラスのインスタンスとして表現されています。例えば、 CharField は文字のフィールドで、 DateTimeField は日時フィー ルドです。こうしたクラスは、各フィールドにどのようなデータ型を記憶させるか を Django に教えます。
Field インスタンスそれぞれの名前(例: question_text や pub_date)は、機械可読なフィールド名です。このフィールド名はPythonコードで使うとともに、データベースも列の名前として使うことになります。
Field の最初の位置引数には、オプションとして人間可読なフィールド名も指定できます。このフィールド名は Django の二つの内省機能で使う他、ドキュメントとしての役割も果たします。人間可読なフィールド名を指定しない場合、 Django は機械可読な名前を使います。上の例では、 Question.pub_date にだけ人間可読なフィールド名を指定しました。モデルの他のフィールドでは、フィールドの機械可読な名前は人間可読な名前としても十分なので定義していません。
Field クラスの中には必須の引数を持つものがありま す。例えば CharField には max_length を指定する必要があります。この引数はデータベーススキーマで使われる他、後で述べるバリデーションでも使われま す。
Field はいくつかオプションの引数も取れます。今回の場合、 votes の default 値を 0 に設定しました。
最後に、 ForeignKey を使用してリレーションシップが定義されていることに注目してください。
これは、それぞれの Choice が一つの Question に関連付けられることを Django に伝えます。 
Django は 多対一、多対多、そして一対一のような一般的なデータベースリレーションシップすべてをサポートします
"""

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    
    def __str__(self):
        return self.question_text # Questionオブジェクトの戻り値をquestion_textにしている
    
    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?'   
    )
    def was_published_recently(self):
        """Bool型の列になる"""
        return timezone.now() >= self.pub_date >= timezone.now() - datetime.timedelta(days=1) # 未来はFalseになるように調整する


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text