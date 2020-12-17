from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404,render
#from django.template import loader
from django.urls import reverse
from django.views import generic

from .models import Choice, Question

#def index(request):
#    latest_question_list = Question.objects.order_by('-pub_date')[:5]
#    content = { 'latest_question_list': latest_question_list}
#    return render(request,'polls_app/index.html',context)
#
#def detail(request,question_id):
#    question = get_object_or_404(Question, pk=question_id)
#    return render(request, 'polls_app/detail.html', {'question': question})
#
#def results(request,question_id):
#    question = get_object_or_404(Question, pk=question_id)
#    return render(request, 'polls_app/results.html', {'question': question})

class IndexView(generic.ListView):
    template_name = 'polls_app/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls_app/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls_app/results.html'


def vote(request,question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls_app/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls_app:results', args=(question.id)))