from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.urls import reverse
from .models import Question, Choice
from django.views import generic


# Каждое представление отвечает за выполнение одного из двух действий:
# возвращение объекта HttpResponse, содержащего ответ для запрашиваемой страницы,
# или создание исключения, такого как Http404.
# Все, чего хочет Джанго, это HttpResponse. Или исключение.

# Каждое общее представление должно знать, на какую модель оно будет воздействовать. Это обеспечивается либо
# с помощью атрибута model (в данном примере model = Question для DetailView и ResultsView), либо путем определения
# метода get_queryset() (как показано в IndexView).

# Для DetailView переменная question для контекста предоставляется автоматически - поскольку мы используем модель
# Django (Question), Django может определить подходящее имя для переменной контекста. Однако для ListView автоматически
# генерируемой переменной контекста является question_list. Чтобы переопределить это, мы предоставляем атрибут context_object_name,
# определяющий, что мы хотим использовать latest_question_list.


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Возвращает пять последних опубликованных вопросов (за исключением тех, которые планируется опубликоваться в будущем)
        """
        q = Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
        print(q.query)
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Исключаются вопросы, которые еще не опубликованы.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'



def vote(request, question_id):
    print(request.POST)
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request,
                      'polls/detail.html',
                      {'question':question,
                              'error_message':'Вы не выбрали вариант ответа'})
    else:
        # selected_choice.votes = F('votes')+1
        selected_choice.votes = selected_choice.votes + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))