from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question  # looks locally in same folder, looks at models.py then import the Question Class

# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")

# ex: /polls/5/
def detail(request, question_id):
    # return HttpResponse("You're looking at question {}".format(question_id))

    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")
    # return render(request, 'polls/detail.html', {'question': question})

    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question_html': question})


# ex: /polls/5/results/
# def results(request, question_id):
#     # a custom return, no need to create a results page, dynamically post basic result
#     # response = "You're looking at the RESULTS of question {}.".format(question_id)
#     # return HttpResponse(response)
#
#
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question_html': question})

# ex: /polls/5/vote/
def vote(request, question_id):
    question_obj = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question_obj.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question_obj,
            'error_message': "You didn't select a CHOICE..CHOICE..CHOICE..CHOICE...",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question_obj.id,)))



# def index(request):
#     latest_question_list_query = Question.objects.order_by('-pub_date')[:5]
#     # template = loader.get_template('polls/index.html')  # not needed if use shortcut
#     context = {
#         'latest_question_list_to_html': latest_question_list_query,
#     }
#     # return HttpResponse(template.render(context, request)) # not needed if use shortcut
#     return render(request, 'polls/index.html', context)

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list_to_html'

    def get_queryset(self):
        """Return the last five published questions.(not including those set to be published in the future)."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class xDetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'