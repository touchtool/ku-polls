from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.utils import timezone
from .models import Choice, Question
from django.contrib import messages


def index(request):
    latest_question_list = Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:]
    text = {"latest_question_list": latest_question_list}
    return render(request, 'polls/index.html', text)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if question.can_vote():
        return render(request, 'polls/detail.html', {'question': question})
    messages.error(request, "Poll doesn't available now")
    return HttpResponseRedirect(reverse('polls:index'))


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        messages.error(request, "You didn't make a choice")
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        messages.success(request, "Your choice is recorded. Thank you for summit.")
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

