from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
# from django.template import loader

from .models import Choice, Question


class IndexView(generic.ListView):
    """ Generic index view. Startview of the polls app which lists the latest questions. """
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """ 
        Return the last five published questions (not including those set to be published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')


class DetailView(generic.DetailView):
    """ Generic detail view. Provides more details to selected question. """
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """ Excludes any questions that aren't published yet. """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    """ Generic results view. Provides the voting results. """
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    '''
    Vote answer to question.
    '''
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing with POST data.
        # This prevents data from being posted twice if a user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
