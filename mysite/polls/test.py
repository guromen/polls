from datetime import timedelta
from http.client import responses

from django.test import TestCase
from django.utils import timezone
from .models import Question
from django.urls import reverse

class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() должен вернуть False для вопросов с pub_date в будущем
        """
        future_question = Question(pub_date = timezone.now() + timedelta(days=30))
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() возвращает False для вопросов, у которых pub_date старше 1 дня
        """
        time = timezone.now() - timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() возвращает True для вопросов, у которых pub_date в пределах 1 дня
        """
        time = timezone.now() - timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

def create_question(question_text, days):
    """
    Создаем вопрос с заданным `question_text` и публикуем его со смещением на
    указанное количество `days` относительно текущего момента (отрицательное значение для вопросов,
     опубликованных в прошлом, положительное для вопросов, которые еще не были опубликованы).
    """
    time = timezone.now() + timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTest(TestCase):
    def test_no_question(self):
        """
        Если вопросов нет, отображается соответствующее сообщение.
        """
        response=self.client.get(reverse('polls:index'))
        self.assertIs(response.status_code, 200)
        self.assertContains(response, 'Нет доступных опросов')
        self.assertQuerySetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Вопросы, дата публикации которых была в прошлом, отображаются на
        индексной странице
        """
        question = create_question('Past question', days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerySetEqual(response.context['latest_question_list'], [question])

    def test_future_question(self):
        """
        Вопросы, у которых дата публикации приходится на будущее, не отображаются на главной странице.
        """
        create_question('Future question', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, 'Нет доступных опросов')
        self.assertQuerySetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Даже если существуют вопросы как из прошлого, так и из будущего, отображаются только вопросы из прошлого.
        """
        past_question = create_question('Past question', days=-30)
        create_question('Future question', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerySetEqual(response.context['latest_question_list'], [past_question])

    def test_two_past_questions(self):
        """
        На странице может отображаться несколько вопросов.
        """
        first_question = create_question('First question', days=-30)
        second_question = create_question('Second question', days=-20)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerySetEqual(response.context['latest_question_list'], [second_question, first_question])

class QuestionDetailViewTest(TestCase):
    """
    При попытке просмотра подробной информации о вопросе с датой публикации в будущем -
    возвращается ошибка 404 (страница не найдена).
    """
    def test_future_question(self):
        future_question = create_question('Future question', days=5)
        response = self.client.get(reverse('polls:detail', args=(future_question.id,)))
        self.assertEquals(response.status_code, 404)

    def test_past_question(self):
        """
        В подробном представлении вопроса с датой публикации в прошлом отображается текст вопроса.
        """
        past_question = create_question('Past question', days=-30)
        response = self.client.get(reverse('polls:detail', args=(past_question.id,)))
        self.assertContains(response, past_question.question_text)