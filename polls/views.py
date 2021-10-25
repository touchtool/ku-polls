"""Render html."""
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from .models import Choice, Question, Votes
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def index(request):
    """Render index questions with index.html."""
    latest_question_list = Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:]
    text = {"latest_question_list": latest_question_list}
    return render(request, 'polls/index.html', text)


def detail(request, question_id):
    """Render selected question with choices."""
    question = get_object_or_404(Question, pk=question_id)
    if question.can_vote():
        return render(request, 'polls/detail.html', {'question': question})
    messages.error(request, "Poll doesn't available now")
    return HttpResponseRedirect(reverse('polls:index'))


def results(request, question_id):
    """Render number of vote each choices."""
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


@login_required(login_url='/accounts/login/')
def vote(request, question_id):
    """Vote method if questions are open."""
    question = get_object_or_404(Question, pk=question_id)
    try:
        choice_id = request.POST['choice']
        selected_choice = question.choice_set.get(pk=choice_id)
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        messages.error(request, "You didn't make a choice")
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        user = request.user

        vote = get_vote_for_user(question, user)

        # case 1: user has not vote for this poll question yet Create Objects
        if not vote:
            vote = Votes(user=user, choice=selected_choice)
        else:
            # case 2: user has already voted. Modify the exist vote and save it.
            vote.choice = selected_choice
        vote.save()

        messages.success(request, "Your choice is recorded. Thank you for summit.")
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def get_vote_for_user(question, user):
    """
    Find and return an existing vote for user on a poll question.

    Returns:
        The user vote
    """
    try:
        votes = Votes.objects.filter(user=user).filter(choice__question=question)
        if votes.count() == 0:
            return None
        else:
            return votes[0]
    except Votes.DoesNotExist:
        return None
