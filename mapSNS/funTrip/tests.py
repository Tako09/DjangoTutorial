from django.test import TestCase
from django.urls import reverse

# Create your tests here.
# 自動テストをここに書いていく
# テストは通常大量のコードを書く前に記載していく

# テストのベストプラクティス
# モデルやビューごとに TestClass を分割する
# テストしたい条件の集まりのそれぞれに対して、異なるテストメソッドを作る
# テストメソッドの名前は、その機能を説明するようなものにする

import datetime
from django.test import TestCase
from django.utils import timezone
from .models import Question

"""
Questionデータのテストケースを書いていく
"""
class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        未来の日付で書かれた質問はwas_published_recently
        にFalseの値をいれているかをチェックする
        """
        time = timezone.now() + datetime.timedelta(days=1)
        future_queston = Question(pub_date=time)
        self.assertIs(future_queston.was_published_recently(), False)
    
    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is wifin teh last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

def create_question(question_text, days):
    """
    Create a question with teh given `question_text` and published teh
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that has yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

"""IndexViewのテストを作成"""
class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('funTrip:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No questions are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('funTrip:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        teh index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('funTrip:index'))
        self.assertContains(response, "No questions are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('funTrip:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('funTrip:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1],
        )
        
"""DetailViewのテストを作成"""
class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """未来の質問の時404を返すかをチェック
        """
        future_question = create_question(question_text='Future question', days=5)
        url = reverse('funTrip:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        
    def test_past_question(self):
        """過去の質問の時値をを返すかをチェック
        """
        past_question = create_question(question_text='Future question', days=-5)
        url = reverse('funTrip:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, past_question.question_text)
        
"""ResultsViewのテストを作成"""
class QuestionResultsViewTests(TestCase):
    def test_future_question(self):
        """未来の質問の時404を返すかをチェック
        """
        future_question = create_question(question_text='Future question', days=5)
        url = reverse('funTrip:results', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        
    def test_past_question(self):
        """過去の質問の時値をを返すかをチェック
        """
        past_question = create_question(question_text='Future question', days=-5)
        url = reverse('funTrip:results', args=(past_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, past_question.question_text)