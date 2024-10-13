from typing import Any
from django.db.models import F
from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.urls import reverse_lazy
from django.views import generic
from django.utils import timezone
from django.views.generic.edit import CreateView, DeleteView
from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    
    #context_object_name="latest_question_list"
    #def get_queryset(self):
    #   return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]

    context_object_name="question_list"
    def get_queryset(self):
        return Question.objects.filter().order_by("-pub_date")

class DetailView(generic.DetailView):
    model=Question
    template_name="polls/detail.html"

class ResultsView(generic.DetailView):
    model=Question
    template_name="polls/results.html"

def vote(request, question_id):
    question=get_object_or_404(Question, pk=question_id)
    try:
        selected_choice=question.choice_set.get(pk=request.POST["choice"])
    except(KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes=F("votes")+1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
    

class QuestionCreateView(CreateView):
    model = Question
    fields = ["question_text", "pub_date"]
    success_url=reverse_lazy("polls:index")

    def form_valid(self, form):
        question=form.save(commit=False)

        question.save()

        choice_texts=self.request.POST.getlist('choice_text')
        for choice_text in choice_texts:
            if choice_text:
                Choice.objects.create(question=question, choice_text=choice_text)

        return super().form_valid(form)


class UpdateQuestion(generic.DetailView):
    model=Question
    template_name="polls/update_question.html"

def putQuestion(request, question_id):
    
    Uquestion = get_object_or_404(Question, pk=question_id)
    selection=request.POST.get('action')
    if selection=='Update':
        Uquestion.question_text = request.POST.get('question_text')
        Uquestion.pub_date = request.POST.get('pub_date')
        choice_texts=request.POST.getlist('choice_text')
        auxQuestions=list(Uquestion.choice_set.all())
        Uquestion.choice_set.all().delete()
        for i, choice_text in enumerate(choice_texts):
                if choice_text:
                    if(i<len(auxQuestions)):
                        Choice.objects.create(question=Uquestion, choice_text=choice_text, votes=auxQuestions[i].votes)
                    else:
                        Choice.objects.create(question=Uquestion, choice_text=choice_text)
        Uquestion.save()
        return HttpResponseRedirect(reverse('polls:detail', args=(Uquestion.id,)))
    elif selection=='Delete':
        Uquestion.delete()
        return HttpResponseRedirect(reverse('polls:index'))



def putChoice(request, choice):
    Uchoice=get_object_or_404(Question, pk=choice.question_id)

